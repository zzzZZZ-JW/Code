from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JointLimit:
    key: str
    label: str
    min_value: float
    max_value: float
    step: float
    max_delta_per_tick: float
    unit: str


JOINT_LIMITS: tuple[JointLimit, ...] = (
    JointLimit("shoulder_pan.pos", "肩部水平旋转", -90.0, 90.0, 1.0, 7.0, "度"),
    JointLimit("shoulder_lift.pos", "肩部俯仰", -90.0, 90.0, 1.0, 7.0, "度"),
    JointLimit("elbow_flex.pos", "肘部弯曲", -90.0, 90.0, 1.0, 7.0, "度"),
    JointLimit("wrist_flex.pos", "腕部俯仰", -90.0, 90.0, 1.0, 8.0, "度"),
    JointLimit("wrist_roll.pos", "腕部旋转", -90.0, 90.0, 1.0, 15.0, "度"),
    JointLimit("gripper.pos", "夹爪开合", 0.0, 1.0, 0.01, 0.04, "比例"),
)

JOINT_KEYS = tuple(limit.key for limit in JOINT_LIMITS)
JOINT_LIMIT_BY_KEY = {limit.key: limit for limit in JOINT_LIMITS}


def clamp_joint(key: str, value: float) -> float:
    limit = JOINT_LIMIT_BY_KEY[key]
    return max(limit.min_value, min(limit.max_value, float(value)))


def to_ui_positions(values: dict[str, float] | None) -> dict[str, float]:
    ui: dict[str, float] = {}
    values = values or {}
    for key in JOINT_KEYS:
        raw = float(values.get(key, 0.0))
        if key == "gripper.pos":
            raw = raw / 100.0
        ui[key] = clamp_joint(key, raw)
    return ui


def to_ui_action(values: dict[str, float] | None) -> dict[str, float]:
    ui: dict[str, float] = {}
    for key, raw_value in (values or {}).items():
        if key not in JOINT_KEYS:
            continue
        raw = float(raw_value)
        if key == "gripper.pos":
            raw = raw / 100.0
        ui[key] = clamp_joint(key, raw)
    return ui


def clamp_ui_positions(values: dict[str, float] | None) -> dict[str, float]:
    values = values or {}
    return {key: clamp_joint(key, float(values.get(key, 0.0))) for key in JOINT_KEYS}


def to_hardware_positions(values: dict[str, float]) -> dict[str, float]:
    hardware: dict[str, float] = {}
    for key in JOINT_KEYS:
        value = clamp_joint(key, float(values.get(key, 0.0)))
        if key == "gripper.pos":
            value *= 100.0
        hardware[key] = value
    return hardware


def to_hardware_action(values: dict[str, float]) -> dict[str, float]:
    hardware: dict[str, float] = {}
    for key, raw_value in values.items():
        if key not in JOINT_KEYS:
            continue
        value = clamp_joint(key, float(raw_value))
        if key == "gripper.pos":
            value *= 100.0
        hardware[key] = value
    return hardware


def zero_positions() -> dict[str, float]:
    positions = {key: 0.0 for key in JOINT_KEYS}
    positions["gripper.pos"] = 0.5
    return positions
