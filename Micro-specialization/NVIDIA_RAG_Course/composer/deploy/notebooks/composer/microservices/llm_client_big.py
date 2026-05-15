"""
LLM Client - Multi-Backend OpenAI Router
Simple, traceable, fail-fast design.

Supports OpenAI-compatible backends (NVIDIA Inference API, NIM, OpenAI)
with AWS Bedrock Converse as a translation-layer fallback.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response, StreamingResponse
from contextlib import asynccontextmanager
from functools import partial, wraps
from typing import Dict, List
import httpx, os, json, logging, asyncio, time, uuid
from opentelemetry import trace

from observability import get_observability

logger, tracer, propagator, traced = get_observability("llm-client")

# HTTP client
Client = partial(httpx.AsyncClient, timeout=httpx.Timeout(connect=10, read=600, write=60, pool=60))

# Global state - computed once on startup
BACKENDS = {}  # url -> {models: {id -> model_data}, key_env: str}
MODEL_MAP = {}  # model_id -> backend_url
INITIAL_KEYS = {k: os.getenv(k) for k in ["NVIDIA_API_KEY", "OPENAI_API_KEY", "AWS_BEARER_TOKEN_BEDROCK"]}

# Bedrock config
BEDROCK_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_BASE_URL = f"https://bedrock-runtime.{BEDROCK_REGION}.amazonaws.com"
BEDROCK_MAX_RETRIES = int(os.getenv("BEDROCK_MAX_RETRIES", "2"))
BEDROCK_RETRY_DELAY = float(os.getenv("BEDROCK_RETRY_DELAY", "1.0"))
BEDROCK_DEFAULT_MAX_TOKENS = int(os.getenv("BEDROCK_DEFAULT_MAX_TOKENS", "16384"))

def get_missing_model_msg(model):
    return {"error": {
        "message": f"The model \'{model}\' does not exist", 
        "type": "invalid_request_error", 
        "param": "model", 
        "code": "model_not_found"}}

# Backend configs - static, validated on startup
BACKEND_CONFIGS = [
    # Primary: NVIDIA Inference API (OpenAI-compat, hosts Claude via AWS)
    {
        "url": "https://inference-api.nvidia.com/v1",
        "key_env": "NVINFR_API_KEY",
        "exclude": [],
        "manual_models": [
            "aws/anthropic/bedrock-claude-opus-4-6",
            "aws/anthropic/bedrock-claude-sonnet-4-6",
        ],
    },
    # NVIDIA NIM (build / integrate API)
    {
        "url": "https://integrate.api.nvidia.com/v1",
        "key_env": "NVIDIA_API_KEY",
        "exclude": [],
    },
    # OpenAI
    {"url": "https://api.openai.com/v1", "key_env": "OPENAI_API_KEY", "exclude": []},
]

# =============================================================================
# BEDROCK CONVERSE TRANSLATION
# =============================================================================

def _coerce_text(content) -> str:
    """Safely coerce content to a string. Handles None, str, list, dict."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return str(content)


def _openai_content_to_bedrock_blocks(content) -> list:
    """Convert OpenAI content (str or array) to Bedrock content blocks."""
    if content is None:
        return []
    if isinstance(content, str):
        if content.strip():
            return [{"text": content}]
        return []
    if isinstance(content, list):
        blocks = []
        for item in content:
            if isinstance(item, str):
                if item.strip():
                    blocks.append({"text": item})
            elif isinstance(item, dict):
                t = item.get("type", "text")
                if t == "text":
                    text = item.get("text", "")
                    if text.strip():
                        blocks.append({"text": text})
                elif t == "image_url":
                    url = item.get("image_url", {}).get("url", "")
                    if url.startswith("data:"):
                        try:
                            header, b64data = url.split(",", 1)
                            media_type = header.split(":")[1].split(";")[0]
                            blocks.append({
                                "image": {
                                    "format": media_type.split("/")[1] if "/" in media_type else "png",
                                    "source": {"bytes": b64data}
                                }
                            })
                        except (ValueError, IndexError):
                            logger.warning(f"Could not parse data URI for image")
                    else:
                        logger.warning(f"Bedrock Converse does not support URL-based images, skipping")
        return blocks
    text = str(content)
    if text.strip():
        return [{"text": text}]
    return []


def _openai_tools_to_bedrock(tools: list) -> dict:
    bedrock_tools = []
    for tool in tools:
        fn = tool.get("function", {})
        spec = {"name": fn.get("name", ""), "description": fn.get("description", "")}
        params = fn.get("parameters")
        if params:
            spec["inputSchema"] = {"json": params}
        bedrock_tools.append({"toolSpec": spec})
    if not bedrock_tools:
        return {}
    return {"toolConfig": {"tools": bedrock_tools}}


def _openai_tool_choice_to_bedrock(tool_choice, tool_config: dict) -> dict:
    if not tool_choice or not tool_config:
        return tool_config
    if isinstance(tool_choice, str):
        if tool_choice == "none":
            return {}
        elif tool_choice == "required":
            tool_config["toolChoice"] = {"any": {}}
        elif tool_choice == "auto":
            tool_config["toolChoice"] = {"auto": {}}
    elif isinstance(tool_choice, dict):
        fn = tool_choice.get("function", {})
        name = fn.get("name", "")
        if name:
            tool_config["toolChoice"] = {"tool": {"name": name}}
    return tool_config


def _merge_consecutive_roles(messages: list) -> list:
    if not messages:
        return messages
    merged = [messages[0]]
    for msg in messages[1:]:
        if msg["role"] == merged[-1]["role"]:
            merged[-1]["content"].extend(msg["content"])
        else:
            merged.append(msg)
    return merged


def _openai_to_bedrock(body: dict) -> dict:
    """Translate OpenAI chat completion request to Bedrock Converse format."""
    messages = body.get("messages", [])
    bedrock_messages, system_parts = [], []

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content")

        if role == "system":
            text = _coerce_text(content)
            if text.strip():
                system_parts.append({"text": text})
            continue

        if role == "tool":
            text = _coerce_text(content)
            tool_result_block = {
                "toolResult": {
                    "toolUseId": msg.get("tool_call_id", ""),
                    "content": [{"text": text if text else "(empty)"}]
                }
            }
            if bedrock_messages and bedrock_messages[-1]["role"] == "user":
                bedrock_messages[-1]["content"].append(tool_result_block)
            else:
                bedrock_messages.append({"role": "user", "content": [tool_result_block]})
            continue

        if role == "assistant" and msg.get("tool_calls"):
            content_blocks = []
            text = _coerce_text(content)
            if text.strip():
                content_blocks.append({"text": text})
            for tc in msg["tool_calls"]:
                fn = tc.get("function", {})
                try:
                    tool_input = json.loads(fn.get("arguments", "{}"))
                except (json.JSONDecodeError, TypeError):
                    tool_input = {}
                content_blocks.append({
                    "toolUse": {
                        "toolUseId": tc.get("id", str(uuid.uuid4())),
                        "name": fn.get("name", ""),
                        "input": tool_input
                    }
                })
            if content_blocks:
                bedrock_messages.append({"role": "assistant", "content": content_blocks})
            continue

        content_blocks = _openai_content_to_bedrock_blocks(content)
        if not content_blocks:
            continue
        bedrock_messages.append({"role": role, "content": content_blocks})

    bedrock_messages = _merge_consecutive_roles(bedrock_messages)
    if not bedrock_messages:
        bedrock_messages = [{"role": "user", "content": [{"text": "(empty)"}]}]

    result = {"messages": bedrock_messages}
    if system_parts:
        result["system"] = system_parts

    config = {}
    if "max_tokens" in body:
        config["maxTokens"] = body["max_tokens"]
    elif "max_completion_tokens" in body:
        config["maxTokens"] = body["max_completion_tokens"]
    else:
        config["maxTokens"] = BEDROCK_DEFAULT_MAX_TOKENS
    if "temperature" in body:
        config["temperature"] = body["temperature"]
    if "top_p" in body:
        config["topP"] = body["top_p"]
    if "stop" in body:
        stop = body["stop"]
        if isinstance(stop, str):
            config["stopSequences"] = [stop]
        elif isinstance(stop, list):
            config["stopSequences"] = stop
    if config:
        result["inferenceConfig"] = config

    tools = body.get("tools")
    if tools:
        tool_config = _openai_tools_to_bedrock(tools)
        tool_choice = body.get("tool_choice")
        if tool_choice:
            tool_config = _openai_tool_choice_to_bedrock(tool_choice, tool_config)
        if tool_config:
            result.update(tool_config)

    return result


def _bedrock_to_openai(resp: dict, model: str) -> dict:
    """Translate Bedrock Converse response to OpenAI chat completion format."""
    output = resp.get("output", {}).get("message", {})
    content_blocks = output.get("content", [])
    usage = resp.get("usage", {})
    stop = resp.get("stopReason", "end_turn")
    finish_map = {"end_turn": "stop", "max_tokens": "length", "stop_sequence": "stop",
                  "tool_use": "tool_calls"}

    text_parts = []
    tool_calls = []
    thinking_text = None
    for block in content_blocks:
        if "text" in block:
            text_parts.append(block["text"])
        elif "toolUse" in block:
            tu = block["toolUse"]
            tool_calls.append({
                "id": tu.get("toolUseId", f"call_{uuid.uuid4().hex[:8]}"),
                "type": "function",
                "function": {
                    "name": tu.get("name", ""),
                    "arguments": json.dumps(tu.get("input", {}))
                }
            })
        elif "reasoningContent" in block:
            rc = block["reasoningContent"]
            if isinstance(rc, dict) and "reasoningText" in rc:
                thinking_text = rc["reasoningText"].get("text", "")
            elif isinstance(rc, dict) and "text" in rc:
                thinking_text = rc["text"]

    text = "".join(text_parts)
    message = {"role": "assistant", "content": text or None}
    if tool_calls:
        message["tool_calls"] = tool_calls

    choice = {"index": 0, "message": message,
              "finish_reason": finish_map.get(stop, "stop")}

    result = {
        "id": f"bedrock-{int(time.time())}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [choice],
        "usage": {"prompt_tokens": usage.get("inputTokens", 0),
                  "completion_tokens": usage.get("outputTokens", 0),
                  "total_tokens": usage.get("totalTokens", 0)}
    }
    if thinking_text:
        result["_thinking"] = thinking_text
    return result


def _is_bedrock_available() -> bool:
    return bool(os.getenv("AWS_BEARER_TOKEN_BEDROCK"))


def _is_retryable_status(status_code: int) -> bool:
    return status_code in (429, 500, 502, 503, 529)


async def proxy_bedrock(body_json: dict, model: str, stream: bool, span) -> Response:
    """Proxy OpenAI-format request to Bedrock Converse endpoint with retries.

    Translates OpenAI → Converse on the way in, Converse → OpenAI on the way out.
    For streaming requests, synthesizes SSE from the non-streaming Converse response.
    Span lifecycle: caller keeps ownership (Converse is non-streaming, fake_stream
    is just serialization of an already-complete response).
    """
    key = os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    bedrock_body = _openai_to_bedrock(body_json)
    url = f"{BEDROCK_BASE_URL}/model/{model}/converse"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    dispatch_span = tracer.start_span(
        "upstream_dispatch",
        context=trace.set_span_in_context(span),
    )
    dispatch_span.set_attribute("bedrock.url", url)
    dispatch_span.set_attribute("bedrock.model", model)
    # dispatch_span.set_attribute("content", json.dumps(body_json))
    dispatch_span.set_attribute("bedrock.content", json.dumps(bedrock_body))
    dispatch_span.end()

    for attempt in range(BEDROCK_MAX_RETRIES + 1):
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(300)) as c:
                r = await c.post(url=url, content=json.dumps(bedrock_body).encode(), headers=headers)

            span.set_attribute("status_code", r.status_code)

            if r.status_code == 200:
                break

            logger.warning(
                f"Bedrock request failed (attempt {attempt + 1}/{BEDROCK_MAX_RETRIES + 1}): "
                f"status={r.status_code} model={model} body={r.text[:500]}"
            )

            if _is_retryable_status(r.status_code) and attempt < BEDROCK_MAX_RETRIES:
                delay = BEDROCK_RETRY_DELAY * (2 ** attempt)
                logger.info(f"Retrying Bedrock request in {delay}s...")
                await asyncio.sleep(delay)
                continue

            span.set_attribute("error", r.text)
            error_body = {
                "error": {
                    "message": f"Bedrock returned {r.status_code}: {r.text[:300]}",
                    "type": "upstream_error",
                    "param": None,
                    "code": f"bedrock_{r.status_code}"
                }
            }
            return Response(
                content=json.dumps(error_body).encode(),
                status_code=r.status_code if r.status_code >= 400 else 502,
                media_type="application/json"
            )

        except httpx.TimeoutException as e:
            logger.warning(f"Bedrock timeout (attempt {attempt + 1}/{BEDROCK_MAX_RETRIES + 1}): {e}")
            if attempt < BEDROCK_MAX_RETRIES:
                delay = BEDROCK_RETRY_DELAY * (2 ** attempt)
                await asyncio.sleep(delay)
                continue
            span.set_attribute("error", f"Timeout after {BEDROCK_MAX_RETRIES + 1} attempts: {e}")
            return Response(
                content=json.dumps({"error": {"message": f"Bedrock request timed out after {BEDROCK_MAX_RETRIES + 1} attempts",
                    "type": "timeout_error", "param": None, "code": "bedrock_timeout"}}).encode(),
                status_code=504, media_type="application/json"
            )

        except httpx.ConnectError as e:
            logger.error(f"Bedrock connection error: {e}")
            span.set_attribute("error", f"Connection error: {e}")
            return Response(
                content=json.dumps({"error": {"message": f"Could not connect to Bedrock: {e}",
                    "type": "connection_error", "param": None, "code": "bedrock_connection_error"}}).encode(),
                status_code=502, media_type="application/json"
            )

    # Success path — translate Converse response back to OpenAI format
    try:
        bedrock_resp = r.json()
        openai_resp = _bedrock_to_openai(bedrock_resp, model)
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Failed to parse Bedrock response: {e}, body: {r.text[:500]}")
        return Response(
            content=json.dumps({"error": {"message": f"Failed to parse Bedrock response: {e}",
                "type": "parse_error", "param": None, "code": "bedrock_parse_error"}}).encode(),
            status_code=502, media_type="application/json"
        )

    span.set_attribute("bedrock.response", json.dumps(bedrock_resp))
    span.set_attribute("content", json.dumps(openai_resp))

    if not stream:
        return Response(content=json.dumps(openai_resp).encode(), status_code=200,
                        media_type="application/json")

    # Synthetic SSE stream from the already-complete Converse response
    async def fake_stream():
        cid = openai_resp["id"]
        msg = openai_resp["choices"][0]["message"]
        finish = openai_resp["choices"][0].get("finish_reason", "stop")

        delta = {"role": "assistant"}
        if msg.get("content"):
            delta["content"] = msg["content"]
        if msg.get("tool_calls"):
            delta["tool_calls"] = msg["tool_calls"]

        yield (f"data: {json.dumps({'id': cid, 'object': 'chat.completion.chunk', 'model': model, 'choices': [{'index': 0, 'delta': delta, 'finish_reason': None}]})}\n\n").encode()
        yield (f"data: {json.dumps({'id': cid, 'object': 'chat.completion.chunk', 'model': model, 'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish}], 'usage': openai_resp.get('usage')})}\n\n").encode()
        yield b"data: [DONE]\n\n"

    return StreamingResponse(fake_stream(), media_type="text/event-stream")

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
                # Fall through to manual_models if any
            elif r.status_code == 200:
                data = r.json().get('data', [])
                models = {m['id']: m for m in data if m['id'] not in config.get('exclude', [])}
            else:
                logger.warning(f"Backend {url} returned {r.status_code}")
    except Exception as e:
        logger.error(f"Failed to validate {url}: {e}")

    # Manual models - always registered even if discovery fails/auth fails
    for mid in config.get("manual_models", []):
        if mid not in models:
            models[mid] = {"id": mid, "object": "model", "owned_by": "manual"}

    if not models:
        return False

    # Store validated backend
    BACKENDS[url] = {"models": models, "key_env": key_env}
    MODEL_MAP.update({mid: url for mid in models.keys()})

    if url == "https://integrate.api.nvidia.com/v1":
        FORCE_MODELS = {
            'nv-rerank-qa-mistral-4b:1': 'https://ai.api.nvidia.com/v1/retrieval/nvidia/reranking',
            'nvidia/llama-3.2-nv-rerankqa-1b-v2': 'https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-3_2-nv-rerankqa-1b-v2/reranking',
            'nvidia/llama-3.2-nemoretriever-500m-rerank-v2': 'https://ai.api.nvidia.com/v1/retrieval/nvidia/llama-3_2-nemoretriever-500m-rerank-v2/reranking',
        }
        MODEL_MAP.update(FORCE_MODELS)
        for mid, murl in FORCE_MODELS.items():
            BACKENDS[murl] = {"models": {mid: {"id": mid}}, "key_env": key_env}
    logger.info(f"✓ {url}: {len(models)} models")
    return True

async def discover_backends():
    """Pre-compute all accessible backends - run once on startup"""
    BACKENDS.clear()
    MODEL_MAP.clear()
    
    results = await asyncio.gather(*[validate_backend(cfg) for cfg in BACKEND_CONFIGS])
    valid_count = sum(results)

    if _is_bedrock_available():
        logger.info(f"✓ Bedrock fallback available (region: {BEDROCK_REGION})")
        valid_count += 1
    
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

app = FastAPI(title="LLM Client", lifespan=lifespan)

@app.get("/health")
async def health():
    return {"backends": len(BACKENDS), "models": len(MODEL_MAP),
            "bedrock_fallback": _is_bedrock_available()}

@app.get("/v1/models")
async def list_models():
    """Aggregates models from all validated backends"""
    all_models = [m for b in BACKENDS.values() for m in b["models"].values()]
    return {"object": "list", "data": all_models}

@app.get("/v1/models/{model:path}")
async def get_model(model: str):
    """Single model lookup"""
    if url := MODEL_MAP.get(model):
        return BACKENDS[url]["models"][model]
    raise HTTPException(404, get_missing_model_msg(model))

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
                        "function": {"name": "", "arguments": ""}
                    }
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

@app.post("/v1/{path:path}")
async def proxy(request: Request, path: str):
    """
    Core proxy logic - simple and traceable:
    1. Parse request body
    2. Lookup backend from MODEL_MAP
    3. If not found but Bedrock credentials exist, route to Bedrock
    4. Forward request with auth
    5. Stream or return response
    """
    body = await request.body()
    span = tracer.start_span("proxy_request")
    span.set_attribute("path", path)
    try:
        try:
            body_json = json.loads(body)
        except Exception as e:
            err_response = dict(status_code=400, detail={"error": f"Malformed JSON {e}"})
            span.set_attribute("error", str(err_response))
            raise HTTPException(**err_response)

        model = body_json.get("model")
        stream = body_json.get("stream", False)
        span.set_attribute("model", model)
        span.set_attribute("stream", stream)

        url = MODEL_MAP.get(model)

        if not url and _is_bedrock_available():
            logger.info(f"Bedrock fallback for unknown model: {model}")
            span.set_attribute("bedrock_fallback", True)
            span.set_attribute("request", json.dumps(body_json))
            return await proxy_bedrock(body_json, model, stream, span)

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
            "accept": "text/event-stream" if stream else "application/json"
        }

        payload_url = url if url.endswith("ranking") else f"{url}/{path}"
        payload = dict(url=payload_url, content=json.dumps(body_json).encode(), headers=headers)

        # NEW: short-lived child span so request phase is published immediately
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

            span.set_attribute("content", r.text[:20000])
            span.set_attribute("status_code", r.status_code)
            return Response(content=r.content, status_code=r.status_code)

        stream_span = span
        span = None  # prevent outer finally from ending it

        async def stream_with_tracing():
            all_chunks = []
            try:
                async with Client().stream("POST", **payload) as r:
                    dispatch_span.set_attribute("status_code", r.status_code)
                    dispatch_span.end()

                    stream_span.set_attribute("status_code", r.status_code)
                    if r.status_code != 200:
                        error_body = await r.aread()
                        stream_span.set_attribute("error", error_body.decode(errors="replace"))
                        yield error_body
                        return

                    async for chunk in r.aiter_bytes():
                        yield chunk
                        all_chunks.append(chunk)
            except httpx.ReadTimeout:
                try:
                    dispatch_span.set_attribute("error", "ReadTimeout before/while opening stream")
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
                        parts = [p for p in raw.split("\ndata: ") if p.strip() and p.strip() != "[DONE]"]
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

@app.post("/rediscover")
async def rediscover():
    """Manually trigger backend rediscovery"""
    await discover_backends()
    return {"backends": len(BACKENDS), "models": len(MODEL_MAP),
            "bedrock_fallback": _is_bedrock_available()}

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