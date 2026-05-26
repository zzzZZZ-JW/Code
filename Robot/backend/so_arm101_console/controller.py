from __future__ import annotations

import asyncio
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any, Literal

from .devices import DevicePair, make_device_pair
from .joints import (
    JOINT_KEYS,
    JOINT_LIMITS,
    clamp_joint,
    to_hardware_action,
    to_hardware_positions,
    to_ui_action,
    to_ui_positions,
    zero_positions,
)
from .ports import PortIdentifier, list_serial_ports
from .safety import apply_joint_safety, invert_ui_action
from .settings import AppSettings, SettingsStore

Mode = Literal["idle", "manual", "teleop"]


class RobotController:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.settings_store = SettingsStore(root / ".runtime" / "settings.json")
        self.settings = self.settings_store.load()
        self.port_identifier = PortIdentifier()
        self.mode: Mode = "idle"
        self.devices: DevicePair | None = None
        self.using_fake = False
        self.joints = zero_positions()
        self.leader_joints = zero_positions()
        self.desired_targets = zero_positions()
        self.sent_targets = zero_positions()
        self.manual_target_keys: set[str] = set()
        self.loop_hz = 0.0
        self._last_tick_at: float | None = None
        self.last_error: str | None = None
        self.emergency_active = False
        self.readable_joints = {"leader": 0, "follower": 0}
        self._lock = asyncio.Lock()
        self._running = False
        self._task: asyncio.Task[None] | None = None
        self._subscribers: set[asyncio.Queue[dict[str, Any]]] = set()

    async def start(self) -> None:
        if self._task is not None:
            return
        self._running = True
        self._task = asyncio.create_task(self._loop(), name="so-arm101-control-loop")

    async def stop(self) -> None:
        self._running = False
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        await self.disconnect()

    async def subscribe(self) -> asyncio.Queue[dict[str, Any]]:
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=4)
        self._subscribers.add(queue)
        await queue.put(await self.snapshot())
        return queue

    def unsubscribe(self, queue: asyncio.Queue[dict[str, Any]]) -> None:
        self._subscribers.discard(queue)

    async def snapshot(self) -> dict[str, Any]:
        async with self._lock:
            return self._snapshot_locked()

    async def save_settings(
        self,
        *,
        leader_port: str | None = None,
        follower_port: str | None = None,
        inversions: dict[str, bool] | None = None,
    ) -> dict[str, Any]:
        async with self._lock:
            if leader_port is not None:
                self.settings.leader_port = leader_port or None
            if follower_port is not None:
                self.settings.follower_port = follower_port or None
            if inversions is not None:
                self.settings.inversions = {
                    key: bool(inversions.get(key, self.settings.inversions.get(key, False)))
                    for key in JOINT_KEYS
                }
            self.settings_store.save(self.settings)
            return self._snapshot_locked()

    async def connect(self, *, use_fake: bool = False) -> dict[str, Any]:
        async with self._lock:
            await self._disconnect_locked()
            self.last_error = None
            self.emergency_active = False
            try:
                pair = make_device_pair(
                    self.settings.leader_port,
                    self.settings.follower_port,
                    use_fake=use_fake,
                )
                await asyncio.to_thread(pair.leader.connect, False)
                await asyncio.to_thread(pair.follower.connect, False)
                self.devices = pair
                self.using_fake = pair.using_fake
                await self._read_devices_locked()
                self.desired_targets = dict(self.joints)
                self.sent_targets = dict(self.joints)
                self.manual_target_keys.clear()
            except Exception as exc:
                self.devices = None
                self.using_fake = False
                self.mode = "idle"
                self.last_error = str(exc)
            return self._snapshot_locked()

    async def disconnect(self) -> dict[str, Any]:
        async with self._lock:
            await self._disconnect_locked()
            return self._snapshot_locked()

    async def emergency_stop(self) -> dict[str, Any]:
        async with self._lock:
            self.mode = "idle"
            self.emergency_active = True
            self.desired_targets = dict(self.joints)
            self.sent_targets = dict(self.joints)
            self.manual_target_keys.clear()
            if self.devices:
                try:
                    await asyncio.to_thread(self.devices.follower.disable_torque)
                except Exception as exc:
                    self.last_error = f"Emergency stop torque disable failed: {exc}"
            return self._snapshot_locked()

    async def reset_stop(self) -> dict[str, Any]:
        async with self._lock:
            self.emergency_active = False
            self.mode = "idle"
            self.desired_targets = dict(self.joints)
            self.sent_targets = dict(self.joints)
            self.manual_target_keys.clear()
            return self._snapshot_locked()

    async def set_mode(self, mode: Mode) -> dict[str, Any]:
        async with self._lock:
            self.last_error = None
            if mode not in {"idle", "manual", "teleop"}:
                raise ValueError(f"Unsupported mode: {mode}")
            if self.emergency_active and mode != "idle":
                raise RuntimeError("Emergency stop is active. Reset it before enabling motion.")
            if mode == "manual" and not self._follower_ready_locked():
                raise RuntimeError("Follower must be connected and calibrated before manual control.")
            if mode == "teleop" and not self._all_ready_locked():
                raise RuntimeError("Leader and follower must be connected and calibrated before teleoperation.")
            self.mode = mode
            if mode in {"idle", "manual"}:
                self.desired_targets = dict(self.joints)
                self.sent_targets = dict(self.joints)
                self.manual_target_keys.clear()
            return self._snapshot_locked()

    async def set_joint_target(self, key: str, value: float) -> dict[str, Any]:
        async with self._lock:
            if key not in JOINT_KEYS:
                raise ValueError(f"Unknown joint: {key}")
            if self.mode != "manual":
                raise RuntimeError("Joint targets can only be changed in manual mode.")
            target_value = clamp_joint(key, float(value))
            self.desired_targets[key] = target_value
            self.joints[key] = target_value
            self.manual_target_keys.add(key)
            return self._snapshot_locked()

    async def start_port_identify(self) -> dict[str, Any]:
        return self.port_identifier.start()

    async def finish_port_identify(self, snapshot_id: str) -> dict[str, Any]:
        return self.port_identifier.finish(snapshot_id)

    def serial_ports_payload(self) -> list[dict[str, Any]]:
        return [asdict(port) for port in list_serial_ports()]

    def command_guides(self) -> dict[str, list[str]]:
        leader = self.settings.leader_port or "<leader-port>"
        follower = self.settings.follower_port or "<follower-port>"
        return {
            "find_port": ["lerobot-find-port"],
            "setup_motors": [
                f"lerobot-setup-motors --robot.type=so101_follower --robot.port={follower}",
                f"lerobot-setup-motors --teleop.type=so101_leader --teleop.port={leader}",
            ],
            "calibrate": [
                f"lerobot-calibrate --robot.type=so101_follower --robot.port={follower} --robot.id=so101_follower_slave",
                f"lerobot-calibrate --teleop.type=so101_leader --teleop.port={leader} --teleop.id=so101_leader_main",
            ],
            "official_teleop_check": [
                (
                    "lerobot-teleoperate --robot.type=so101_follower "
                    f"--robot.port={follower} --robot.id=so101_follower_slave "
                    "--teleop.type=so101_leader "
                    f"--teleop.port={leader} --teleop.id=so101_leader_main --fps=30"
                )
            ],
        }

    async def _loop(self) -> None:
        while self._running:
            started = time.perf_counter()
            if self._last_tick_at is not None:
                period = max(started - self._last_tick_at, 1e-6)
                self.loop_hz = 1.0 / period
            self._last_tick_at = started
            payload: dict[str, Any] | None = None
            async with self._lock:
                try:
                    if self.devices is not None:
                        if self.mode == "manual" and not self.emergency_active:
                            await self._send_manual_step_locked()
                        elif self.mode == "teleop" and not self.emergency_active:
                            await self._read_devices_locked()
                            await self._send_teleop_step_locked()
                    payload = self._snapshot_locked()
                except Exception as exc:
                    self.last_error = str(exc)
                    self.mode = "idle"
                    payload = self._snapshot_locked()
            if payload is not None:
                self._publish(payload)
            await asyncio.sleep(max(1.0 / 30.0 - (time.perf_counter() - started), 0.005))

    async def _send_manual_step_locked(self) -> None:
        if not self.devices or not self.manual_target_keys:
            return
        safe: dict[str, float] = {}
        for key in self.manual_target_keys:
            safe[key] = clamp_joint(key, float(self.desired_targets.get(key, self.joints.get(key, 0.0))))
        self.joints.update(safe)
        sent = await asyncio.to_thread(self.devices.follower.send_action, to_hardware_action(safe))
        self.sent_targets.update(to_ui_action(sent))
        self.manual_target_keys.difference_update(safe)

    async def _send_teleop_step_locked(self) -> None:
        if not self.devices:
            return
        action = await asyncio.to_thread(self.devices.leader.get_action)
        self.leader_joints = to_ui_positions(action)
        target = invert_ui_action(self.leader_joints, self.settings.inversions)
        self.desired_targets = target
        safe = apply_joint_safety(self.joints, target)
        sent = await asyncio.to_thread(self.devices.follower.send_action, to_hardware_positions(safe))
        self.sent_targets = to_ui_positions(sent)

    async def _read_devices_locked(self) -> None:
        if not self.devices:
            return
        follower_obs = await asyncio.to_thread(self.devices.follower.get_observation)
        self.joints = to_ui_positions(follower_obs)
        self.readable_joints["follower"] = len([key for key in JOINT_KEYS if key in follower_obs])
        leader_action = await asyncio.to_thread(self.devices.leader.get_action)
        self.leader_joints = to_ui_positions(leader_action)
        self.readable_joints["leader"] = len([key for key in JOINT_KEYS if key in leader_action])

    async def _disconnect_locked(self) -> None:
        self.mode = "idle"
        self.manual_target_keys.clear()
        if self.devices is not None:
            for device in (self.devices.follower, self.devices.leader):
                try:
                    await asyncio.to_thread(device.disconnect)
                except Exception as exc:
                    self.last_error = f"Disconnect warning: {exc}"
        self.devices = None
        self.using_fake = False
        self.readable_joints = {"leader": 0, "follower": 0}

    def _snapshot_locked(self) -> dict[str, Any]:
        leader_connected = bool(self.devices and self.devices.leader.is_connected)
        follower_connected = bool(self.devices and self.devices.follower.is_connected)
        leader_calibrated = self.devices.leader.is_calibrated if self.devices else None
        follower_calibrated = self.devices.follower.is_calibrated if self.devices else None
        return {
            "mode": self.mode,
            "ports": {
                "leader": self.settings.leader_port,
                "follower": self.settings.follower_port,
            },
            "connected": {
                "leader": leader_connected,
                "follower": follower_connected,
            },
            "calibrated": {
                "leader": leader_calibrated,
                "follower": follower_calibrated,
            },
            "ready": {
                "manual": self._follower_ready_locked(),
                "teleop": self._all_ready_locked(),
            },
            "joints": dict(self.joints),
            "leaderJoints": dict(self.leader_joints),
            "targets": dict(self.desired_targets),
            "sentTargets": dict(self.sent_targets),
            "jointLimits": [asdict(limit) for limit in JOINT_LIMITS],
            "inversions": {key: bool(self.settings.inversions.get(key, False)) for key in JOINT_KEYS},
            "loopHz": round(self.loop_hz, 1),
            "lastError": self.last_error,
            "usingFake": self.using_fake,
            "emergencyActive": self.emergency_active,
            "readableJoints": dict(self.readable_joints),
            "guides": self.command_guides(),
        }

    def _follower_ready_locked(self) -> bool:
        return bool(self.devices and self.devices.follower.is_connected and self.devices.follower.is_calibrated)

    def _all_ready_locked(self) -> bool:
        return bool(
            self.devices
            and self.devices.leader.is_connected
            and self.devices.follower.is_connected
            and self.devices.leader.is_calibrated
            and self.devices.follower.is_calibrated
        )

    def _publish(self, payload: dict[str, Any]) -> None:
        for queue in list(self._subscribers):
            if queue.full():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    pass
            try:
                queue.put_nowait(payload)
            except asyncio.QueueFull:
                pass
