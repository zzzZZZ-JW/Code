from __future__ import annotations

import math
import os
import time
from dataclasses import dataclass
from typing import Protocol

from .joints import JOINT_KEYS, JOINT_LIMIT_BY_KEY, to_hardware_positions, zero_positions


class ArmDevice(Protocol):
    @property
    def is_connected(self) -> bool: ...

    @property
    def is_calibrated(self) -> bool: ...

    def connect(self, calibrate: bool = False) -> None: ...

    def disconnect(self) -> None: ...

    def disable_torque(self) -> None: ...


class FollowerDevice(ArmDevice, Protocol):
    def get_observation(self) -> dict[str, float]: ...

    def send_action(self, action: dict[str, float]) -> dict[str, float]: ...


class LeaderDevice(ArmDevice, Protocol):
    def get_action(self) -> dict[str, float]: ...


class HardwareUnavailableError(RuntimeError):
    pass


@dataclass(frozen=True)
class DevicePair:
    leader: LeaderDevice
    follower: FollowerDevice
    using_fake: bool


class FakeFollower:
    def __init__(self) -> None:
        self._connected = False
        self._current = to_hardware_positions(zero_positions())
        self._target = dict(self._current)

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def is_calibrated(self) -> bool:
        return True

    def connect(self, calibrate: bool = False) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def disable_torque(self) -> None:
        self._target = dict(self._current)

    def get_observation(self) -> dict[str, float]:
        self._ensure_connected()
        for key in JOINT_KEYS:
            max_delta = JOINT_LIMIT_BY_KEY[key].max_delta_per_tick
            if key == "gripper.pos":
                max_delta *= 100.0
            current = self._current[key]
            target = self._target[key]
            if target > current + max_delta:
                current += max_delta
            elif target < current - max_delta:
                current -= max_delta
            else:
                current = target
            self._current[key] = current
        return dict(self._current)

    def send_action(self, action: dict[str, float]) -> dict[str, float]:
        self._ensure_connected()
        for key in JOINT_KEYS:
            if key in action:
                self._target[key] = float(action[key])
        return dict(self._target)

    def _ensure_connected(self) -> None:
        if not self._connected:
            raise RuntimeError("Fake follower is not connected.")


class FakeLeader:
    def __init__(self) -> None:
        self._connected = False
        self._started_at = time.perf_counter()

    @property
    def is_connected(self) -> bool:
        return self._connected

    @property
    def is_calibrated(self) -> bool:
        return True

    def connect(self, calibrate: bool = False) -> None:
        self._connected = True
        self._started_at = time.perf_counter()

    def disconnect(self) -> None:
        self._connected = False

    def disable_torque(self) -> None:
        return None

    def get_action(self) -> dict[str, float]:
        if not self._connected:
            raise RuntimeError("Fake leader is not connected.")
        t = time.perf_counter() - self._started_at
        return {
            "shoulder_pan.pos": 55.0 * math.sin(t * 0.55),
            "shoulder_lift.pos": 38.0 * math.sin(t * 0.45 + 0.7),
            "elbow_flex.pos": -55.0 + 45.0 * math.sin(t * 0.5 + 1.4),
            "wrist_flex.pos": 42.0 * math.sin(t * 0.8 + 0.2),
            "wrist_roll.pos": 95.0 * math.sin(t * 0.7),
            "gripper.pos": 50.0 + 45.0 * math.sin(t * 0.9),
        }


class RealFollower:
    def __init__(self, port: str, arm_id: str) -> None:
        SO101Follower, SO101FollowerConfig, _, _ = _load_lerobot_classes()
        self._device = SO101Follower(
            SO101FollowerConfig(
                port=port,
                id=arm_id,
                use_degrees=True,
                max_relative_target=None,
            )
        )

    @property
    def is_connected(self) -> bool:
        return bool(self._device.is_connected)

    @property
    def is_calibrated(self) -> bool:
        return bool(self._device.is_calibrated)

    def connect(self, calibrate: bool = False) -> None:
        self._device.connect(calibrate=calibrate)
        _sync_cached_calibration_from_motors(self._device)

    def disconnect(self) -> None:
        self._device.disconnect()

    def disable_torque(self) -> None:
        if hasattr(self._device, "disable_torque"):
            self._device.disable_torque()
        elif hasattr(self._device, "bus"):
            self._device.bus.disable_torque()

    def get_observation(self) -> dict[str, float]:
        observation = self._device.get_observation()
        return {key: float(observation[key]) for key in JOINT_KEYS if key in observation}

    def send_action(self, action: dict[str, float]) -> dict[str, float]:
        sent = self._device.send_action(action)
        return {key: float(sent[key]) for key in JOINT_KEYS if key in sent}


class RealLeader:
    def __init__(self, port: str, arm_id: str) -> None:
        _, _, SO101Leader, SO101LeaderConfig = _load_lerobot_classes()
        self._device = SO101Leader(SO101LeaderConfig(port=port, id=arm_id, use_degrees=True))

    @property
    def is_connected(self) -> bool:
        return bool(self._device.is_connected)

    @property
    def is_calibrated(self) -> bool:
        return bool(self._device.is_calibrated)

    def connect(self, calibrate: bool = False) -> None:
        self._device.connect(calibrate=calibrate)
        _sync_cached_calibration_from_motors(self._device)

    def disconnect(self) -> None:
        self._device.disconnect()

    def disable_torque(self) -> None:
        if hasattr(self._device, "disable_torque"):
            self._device.disable_torque()
        elif hasattr(self._device, "bus"):
            self._device.bus.disable_torque()

    def get_action(self) -> dict[str, float]:
        action = self._device.get_action()
        return {key: float(action[key]) for key in JOINT_KEYS if key in action}


def make_device_pair(
    leader_port: str | None,
    follower_port: str | None,
    *,
    use_fake: bool = False,
) -> DevicePair:
    env_fake = os.getenv("SO_ARM101_FAKE", "").lower() in {"1", "true", "yes"}
    if use_fake or env_fake:
        return DevicePair(FakeLeader(), FakeFollower(), using_fake=True)
    if not leader_port or not follower_port:
        raise ValueError("Leader and follower ports are required for real hardware mode.")
    _load_lerobot_classes()
    return DevicePair(
        leader=RealLeader(leader_port, "so101_leader_main"),
        follower=RealFollower(follower_port, "so101_follower_slave"),
        using_fake=False,
    )


def _load_lerobot_classes():
    try:
        try:
            from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
        except ImportError:
            from lerobot.robots.so_follower.config_so_follower import SO101FollowerConfig
            from lerobot.robots.so_follower.so_follower import SO101Follower

        try:
            from lerobot.teleoperators.so_leader import SO101Leader, SO101LeaderConfig
        except ImportError:
            from lerobot.teleoperators.so_leader.config_so_leader import SO101LeaderConfig
            from lerobot.teleoperators.so_leader.so_leader import SO101Leader
    except ImportError as exc:
        raise HardwareUnavailableError(
            "LeRobot is not installed. Run `uv sync --extra hardware` before using real arms."
        ) from exc
    return SO101Follower, SO101FollowerConfig, SO101Leader, SO101LeaderConfig


def _sync_cached_calibration_from_motors(device) -> None:
    bus = getattr(device, "bus", None)
    if bus is None:
        return
    try:
        if device.is_calibrated:
            return
    except Exception:
        pass

    calibration = bus.read_calibration()
    if set(calibration) != set(bus.motors):
        return

    device.calibration = calibration
    bus.calibration = calibration
    if hasattr(device, "_save_calibration"):
        device._save_calibration()
