"""
LLM Client - NVIDIA-Only OpenAI Router (Teaching/Toy Version)

Simple, traceable, fail-fast design.

- Discovers models from NVIDIA Inference API and NVIDIA Integrate API
- Routes /v1/* requests to the correct NVIDIA backend based on `model`
- Preserves full tracing behavior:
  - root span per request
  - child span for upstream dispatch
  - streaming span with merged SSE summary for trace
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response, StreamingResponse
from contextlib import asynccontextmanager
from functools import partial
from typing import Dict
import httpx, os, json, logging, asyncio, time

from opentelemetry import trace
from observability import get_observability

logger, tracer, propagator, traced = get_observability("llm-client")

# HTTP client
Client = partial(
    httpx.AsyncClient,
    timeout=httpx.Timeout(connect=10, read=600, write=60, pool=60),
)

# Global state - computed once on startup
BACKENDS: Dict[str, Dict] = {}   # url -> {models: {id -> model_data}, key_env: str}
MODEL_MAP: Dict[str, str] = {}   # model_id -> backend_url
INITIAL_KEYS = {
    k: os.getenv(k) for k in ["NVINFR_API_KEY", "NVIDIA_API_KEY"]
}

def get_missing_model_msg(model):
    return {
        "error": {
            "message": f"The model '{model}' does not exist",
            "type": "invalid_request_error",
            "param": "model",
            "code": "model_not_found",
        }
    }

# Backend configs - NVIDIA only
BACKEND_CONFIGS = [
    # NVIDIA Inference API (can host multiple families)
    {
        "url": "https://inference-api.nvidia.com/v1",
        "key_env": "NVINFR_API_KEY",
        "exclude": [],
        "manual_models": [],
    },
    # NVIDIA NIM (build / integrate API)
    {
        "url": "https://integrate.api.nvidia.com/v1",
        "key_env": "NVIDIA_API_KEY",
        "exclude": [],
        "manual_models": [],
    },
]

# =============================================================================
# BACKEND DISCOVERY
# =============================================================================

async def validate_backend(config: Dict) -> bool:
    """
    Validate backend is accessible and has valid auth.
    Returns False on permission errors - backend will be ejected.
    """
    url, key_env = config["url"], config["key_env"]
    key = os.getenv(key_env)

    if not key:
        logger.warning(f"No key for {url} - skipping")
        return False

    models = {}

    # Auto-discover from /models endpoint
    try:
        async with Client() as c:
            headers = {"authorization": f"Bearer {key}"}
            r = await c.get(f"{url}/models", headers=headers, timeout=10.0)

            # Permission errors = permanent failure
            if r.status_code in [401, 403]:
                logger.error(f"Auth failed for {url} - ejecting backend")
            elif r.status_code == 200:
                data = r.json().get("data", [])
                models = {
                    m["id"]: m
                    for m in data
                    if m["id"] not in config.get("exclude", [])
                }
            else:
                logger.warning(f"Backend {url} returned {r.status_code}")
    except Exception as e:
        logger.error(f"Failed to validate {url}: {e}")

    # Manual models - always registered even if discovery fails/auth fails
    for mid in config.get("manual_models", []):
        if mid not in models:
            models[mid] = {
                "id": mid,
                "object": "model",
                "owned_by": "manual",
            }

    if not models:
        return False

    # Store validated backend
    BACKENDS[url] = {"models": models, "key_env": key_env}
    MODEL_MAP.update({mid: url for mid in models.keys()})

    # Special routing for rerank endpoints under integrate.api.nvidia.com
    if url == "https://integrate.api.nvidia.com/v1":
        FORCE_MODELS = {
            "nv-rerank-qa-mistral-4b:1": "https://ai.api.nvidia.com/v1/retrieval/nvidia/reranking",
            "nvidia/llama-3.2-nv-rerankqa-1b-v2": "https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-3_2-nv-rerankqa-1b-v2/reranking",
            "nvidia/llama-3.2-nemoretriever-500m-rerank-v2": "https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-3_2-nemoretriever-500m-rerank-v2/reranking",
        }
        MODEL_MAP.update(FORCE_MODELS)
        for mid, murl in FORCE_MODELS.items():
            BACKENDS[murl] = {"models": {mid: {"id": mid}}, "key_env": key_env}

    logger.info(f"✓ {url}: {len(models)} models")
    return True

async def discover_backends():
    """Pre-compute all accessible backends - run once on startup."""
    BACKENDS.clear()
    MODEL_MAP.clear()

    results = await asyncio.gather(
        *[validate_backend(cfg) for cfg in BACKEND_CONFIGS]
    )
    valid_count = sum(results)

    if valid_count == 0:
        logger.error("No backends available!")
    else:
        logger.info(f"Ready: {valid_count} backends, {len(MODEL_MAP)} models")
    return results

# Lifecycle - clean and simple
@asynccontextmanager
async def lifespan(app: FastAPI):
    await discover_backends()
    yield

app = FastAPI(title="LLM Client (NVIDIA-only)", lifespan=lifespan)

# =============================================================================
# HEALTH + MODELS
# =============================================================================

@app.get("/health")
async def health():
    return {
        "backends": len(BACKENDS),
        "models": len(MODEL_MAP),
    }

@app.get("/v1/models")
async def list_models():
    """Aggregates models from all validated backends."""
    all_models = [m for b in BACKENDS.values() for m in b["models"].values()]
    return {"object": "list", "data": all_models}

@app.get("/v1/models/{model:path}")
async def get_model(model: str):
    """Single model lookup."""
    if url := MODEL_MAP.get(model):
        return BACKENDS[url]["models"][model]
    raise HTTPException(404, get_missing_model_msg(model))

# =============================================================================
# STREAM CHUNK MERGE (TRACE SUMMARY)
# =============================================================================

def merge_openai_chunks(chunks: dict[int, dict]) -> dict:
    content = []
    tool_calls = {}
    usage = None
    first = chunks.get(0, {})
    text_class = ""
    acc_choice = {"index": 0}

    for _, c in chunks.items():
        if not c or not c.get("choices"):
            continue

        choice = c["choices"][0]

        if "delta" in choice:
            delta = choice.get("delta", {})

            if "content" in delta and delta["content"]:
                content.append(delta["content"])
                text_class = "content"

            for tc in delta.get("tool_calls", []) or []:
                idx = tc.get("index", 0)
                entry = tool_calls.setdefault(
                    idx,
                    {
                        "id": "",
                        "type": "function",
                        "function": {"name": "", "arguments": ""},
                    },
                )

                if tc.get("id"):
                    entry["id"] = tc["id"]
                if tc.get("type"):
                    entry["type"] = tc["type"]

                fn = tc.get("function", {})
                if fn.get("name"):
                    entry["function"]["name"] = fn["name"]
                if fn.get("arguments"):
                    entry["function"]["arguments"] += fn["arguments"]

        elif "text" in choice:
            content.append(choice.get("text", ""))
            text_class = "text"

        usage = c.get("usage", usage)
        if choice.get("finish_reason"):
            acc_choice["finish_reason"] = choice["finish_reason"]
            acc_choice["stop_reason"] = choice.get("stop_reason")

    if text_class == "content":
        msg = {"role": "assistant", "content": "".join(content)}
        if tool_calls:
            msg["tool_calls"] = [tool_calls[i] for i in sorted(tool_calls)]
        acc_choice["message"] = msg
    elif text_class == "text":
        acc_choice["text"] = "".join(content)

    return {
        "id": first.get("id", "synthetic"),
        "object": first.get("object", "chat.completion"),
        "created": first.get("created"),
        "model": first.get("model"),
        "choices": [acc_choice],
        "usage": usage,
        "num_chunks": len(chunks),
    }

# =============================================================================
# CORE PROXY (WITH FULL TRACE)
# =============================================================================

@app.post("/v1/{path:path}")
async def proxy(request: Request, path: str):
    """
    Core proxy logic - simple and traceable:
      1. Parse request body
      2. Lookup backend from MODEL_MAP
      3. Forward request with auth
      4. Stream or return response

    Tracing:
      - Root span per request: "proxy_request"
      - Child span for upstream dispatch: "upstream_dispatch"
      - Streaming span captures full merged content for traces
    """
    body = await request.body()
    span = tracer.start_span("proxy_request")
    span.set_attribute("path", path)

    try:
        try:
            body_json = json.loads(body)
        except Exception as e:
            err_response = dict(
                status_code=400,
                detail={"error": f"Malformed JSON {e}"},
            )
            span.set_attribute("error", str(err_response))
            raise HTTPException(**err_response)

        model = body_json.get("model")
        stream = body_json.get("stream", False)
        span.set_attribute("model", model)
        span.set_attribute("stream", stream)

        url = MODEL_MAP.get(model)

        if not url:
            err_response = dict(status_code=400, detail=get_missing_model_msg(model))
            span.set_attribute("error", str(err_response))
            raise HTTPException(**err_response)

        backend = BACKENDS[url]
        span.set_attribute("backend_url", url)
        key = os.getenv(backend["key_env"])
        span.set_attribute("request", json.dumps(body_json))

        headers = {
            "authorization": f"Bearer {key}",
            "content-type": "application/json",
            "accept": "text/event-stream" if stream else "application/json",
        }

        payload_url = url if url.endswith("ranking") else f"{url}/{path}"
        payload = dict(
            url=payload_url,
            content=json.dumps(body_json).encode(),
            headers=headers,
        )

        # Child span for upstream dispatch
        dispatch_span = tracer.start_span(
            "upstream_dispatch",
            context=trace.set_span_in_context(span),
        )
        dispatch_span.set_attribute("backend_url", payload_url)
        dispatch_span.set_attribute("model", model)
        dispatch_span.set_attribute("stream", stream)
        dispatch_span.set_attribute("content", json.dumps(body_json))

        if not stream:
            try:
                async with Client() as c:
                    r = await c.post(**payload)
                dispatch_span.set_attribute("status_code", r.status_code)
            except Exception as e:
                dispatch_span.set_attribute("error", str(e))
                raise
            finally:
                dispatch_span.end()

            span.set_attribute("content", r.text)
            span.set_attribute("status_code", r.status_code)
            return Response(content=r.content, status_code=r.status_code)

        # Streaming path: separate stream_span
        stream_span = span
        span = None  # prevent outer finally from ending it twice

        async def stream_with_tracing():
            all_chunks = []
            try:
                async with Client().stream("POST", **payload) as r:
                    dispatch_span.set_attribute("status_code", r.status_code)
                    dispatch_span.end()

                    stream_span.set_attribute("status_code", r.status_code)
                    if r.status_code != 200:
                        error_body = await r.aread()
                        stream_span.set_attribute(
                            "error", error_body.decode(errors="replace")
                        )
                        yield error_body
                        return

                    async for chunk in r.aiter_bytes():
                        yield chunk
                        all_chunks.append(chunk)
            except httpx.ReadTimeout:
                try:
                    dispatch_span.set_attribute(
                        "error", "ReadTimeout before/while opening stream"
                    )
                    dispatch_span.end()
                except Exception:
                    pass
                stream_span.set_attribute("error", "ReadTimeout during streaming")
                logger.error(f"ReadTimeout streaming {model} from {url}")
                return
            except Exception as e:
                try:
                    dispatch_span.set_attribute("error", str(e))
                    dispatch_span.end()
                except Exception:
                    pass
                stream_span.set_attribute("error", str(e))
                logger.error(f"Stream error for {model}: {e}")
                return
            finally:
                if all_chunks:
                    try:
                        raw = b"".join(all_chunks).decode(errors="replace")
                        parts = [
                            p
                            for p in raw.split("\ndata: ")
                            if p.strip() and p.strip() != "[DONE]"
                        ]
                        if parts and parts[0].startswith("data: "):
                            parts[0] = parts[0][6:]
                        parsed = {}
                        for i, p in enumerate(parts):
                            p = p.rstrip("\n")
                            if not p:
                                continue
                            try:
                                parsed[i] = json.loads(p)
                            except json.JSONDecodeError:
                                continue
                        if parsed:
                            summary = merge_openai_chunks(parsed)
                            stream_span.set_attribute("content", json.dumps(summary))
                    except Exception as e:
                        logger.warning(f"Trace aggregation: {e}")
                stream_span.end()

        gen = stream_with_tracing()

        try:
            first_chunk = await gen.__anext__()
        except StopAsyncIteration:
            raise HTTPException(status_code=502, detail="Empty upstream response")

        if isinstance(first_chunk, bytes) and first_chunk.startswith(b'{"error'):
            try:
                err = json.loads(first_chunk)
                await gen.aclose()
                raise HTTPException(status_code=502, detail=err)
            except (json.JSONDecodeError, HTTPException):
                raise

        async def prepend_first():
            yield first_chunk
            async for chunk in gen:
                yield chunk

        return StreamingResponse(prepend_first(), media_type="text/event-stream")

    finally:
        if span is not None:
            span.end()

# =============================================================================
# Rediscovery helper (unchanged behavior, but NVIDIA-only)
# =============================================================================

@app.post("/rediscover")
async def rediscover():
    """Manually trigger backend rediscovery."""
    await discover_backends()
    return {
        "backends": len(BACKENDS),
        "models": len(MODEL_MAP),
    }

if __name__ == "__main__":
    import uvicorn

    DEBUG_MODE = os.getenv("DEBUG", "0") == "1"
    log_level = "debug" if DEBUG_MODE else "info"

    uvicorn.run(
        "llm_client:app",
        host="0.0.0.0",
        port=9000,
        log_level=log_level,
    )
