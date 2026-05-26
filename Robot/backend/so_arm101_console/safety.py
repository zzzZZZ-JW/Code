from __future__ import annotations

from .joints import JOINT_KEYS, JOINT_LIMIT_BY_KEY, clamp_joint


def limit_single_step(current: float, target: float, max_delta: float) -> float:
    if target > current + max_delta:
        return current + max_delta
    if target < current - max_delta:
        return current - max_delta
    return target


def apply_joint_safety(current: dict[str, float], target: dict[str, float]) -> dict[str, float]:
    safe: dict[str, float] = {}
    for key in JOINT_KEYS:
        limit = JOINT_LIMIT_BY_KEY[key]
        current_value = clamp_joint(key, float(current.get(key, 0.0)))
        target_value = clamp_joint(key, float(target.get(key, current_value)))
        safe[key] = clamp_joint(
            key,
            limit_single_step(current_value, target_value, limit.max_delta_per_tick),
        )
    return safe


def invert_ui_action(values: dict[str, float], inversions: dict[str, bool]) -> dict[str, float]:
    result: dict[str, float] = {}
    for key in JOINT_KEYS:
        value = float(values.get(key, 0.0))
        if inversions.get(key, False):
            value = 1.0 - value if key == "gripper.pos" else -value
        result[key] = clamp_joint(key, value)
    return result

