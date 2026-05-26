from __future__ import annotations

import mimetypes
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .controller import Mode, RobotController

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FRONTEND_DIST = PROJECT_ROOT / "frontend" / "dist"
mimetypes.add_type("model/gltf-binary", ".glb")
controller = RobotController(PROJECT_ROOT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await controller.start()
    try:
        yield
    finally:
        await controller.stop()


app = FastAPI(title="SO-ARM101 Local Console", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SettingsUpdate(BaseModel):
    leader_port: str | None = None
    follower_port: str | None = None
    inversions: dict[str, bool] | None = None


class ConnectRequest(BaseModel):
    use_fake: bool = False


class ModeRequest(BaseModel):
    mode: Literal["idle", "manual", "teleop"]


class JointTargetRequest(BaseModel):
    value: float


class IdentifyFinishRequest(BaseModel):
    snapshot_id: str


@app.get("/api/health")
async def health():
    return {"ok": True}


@app.get("/api/state")
async def get_state():
    return await controller.snapshot()


@app.get("/api/ports")
async def get_ports():
    return {"ports": controller.serial_ports_payload()}


@app.post("/api/ports/identify/start")
async def start_port_identify():
    return await controller.start_port_identify()


@app.post("/api/ports/identify/finish")
async def finish_port_identify(request: IdentifyFinishRequest):
    return await controller.finish_port_identify(request.snapshot_id)


@app.get("/api/guides")
async def guides():
    return controller.command_guides()


@app.put("/api/settings")
async def update_settings(request: SettingsUpdate):
    return await controller.save_settings(
        leader_port=request.leader_port,
        follower_port=request.follower_port,
        inversions=request.inversions,
    )


@app.post("/api/connect")
async def connect(request: ConnectRequest):
    return await controller.connect(use_fake=request.use_fake)


@app.post("/api/disconnect")
async def disconnect():
    return await controller.disconnect()


@app.post("/api/stop")
async def emergency_stop():
    return await controller.emergency_stop()


@app.post("/api/stop/reset")
async def reset_stop():
    return await controller.reset_stop()


@app.post("/api/mode")
async def set_mode(request: ModeRequest):
    try:
        return await controller.set_mode(request.mode)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/joints/{joint_key:path}/target")
async def set_joint_target(joint_key: str, request: JointTargetRequest):
    key = joint_key if joint_key.endswith(".pos") else f"{joint_key}.pos"
    try:
        return await controller.set_joint_target(key, request.value)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.websocket("/ws")
async def websocket_state(websocket: WebSocket):
    await websocket.accept()
    queue = await controller.subscribe()
    try:
        while True:
            payload = await queue.get()
            await websocket.send_json(payload)
    except WebSocketDisconnect:
        controller.unsubscribe(queue)
    except Exception:
        controller.unsubscribe(queue)
        raise


if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")
    models_dir = FRONTEND_DIST / "models"
    if models_dir.exists():
        app.mount("/models", StaticFiles(directory=models_dir), name="models")


@app.get("/")
async def root():
    index = FRONTEND_DIST / "index.html"
    if index.exists():
        return FileResponse(index)
    return {
        "name": "SO-ARM101 Local Console",
        "frontend": "Run `npm run dev --prefix frontend` during development.",
    }


@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    index = FRONTEND_DIST / "index.html"
    if full_path.startswith("api/") or full_path == "ws":
        raise HTTPException(status_code=404, detail="Not found")
    if index.exists():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="Frontend build not found")


def create_app() -> FastAPI:
    return app
