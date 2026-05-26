from so_arm101_console.joints import (
    clamp_joint,
    clamp_ui_positions,
    to_hardware_action,
    to_hardware_positions,
    to_ui_action,
    to_ui_positions,
)
from so_arm101_console.safety import apply_joint_safety, invert_ui_action


def test_joint_clamping_and_gripper_mapping():
    assert clamp_joint("shoulder_pan.pos", 300) == 90
    assert clamp_joint("elbow_flex.pos", -300) == -90

    hardware = to_hardware_positions({"gripper.pos": 0.5})
    assert hardware["gripper.pos"] == 50

    partial_hardware = to_hardware_action({"gripper.pos": 0.5})
    assert partial_hardware == {"gripper.pos": 50}

    ui = to_ui_positions({"gripper.pos": 25})
    assert ui["gripper.pos"] == 0.25

    partial_ui = to_ui_action({"gripper.pos": 25})
    assert partial_ui == {"gripper.pos": 0.25}

    clamped_ui = clamp_ui_positions({"gripper.pos": 0.25, "shoulder_pan.pos": 300})
    assert clamped_ui["gripper.pos"] == 0.25
    assert clamped_ui["shoulder_pan.pos"] == 90


def test_step_limiter_prevents_large_jumps():
    current = {"shoulder_pan.pos": 0, "gripper.pos": 0.0}
    target = {"shoulder_pan.pos": 140, "gripper.pos": 1.0}

    safe = apply_joint_safety(current, target)

    assert safe["shoulder_pan.pos"] == 7
    assert safe["gripper.pos"] == 0.04


def test_teleop_inversions_are_applied_in_ui_units():
    values = {"shoulder_lift.pos": 45, "gripper.pos": 0.2}

    inverted = invert_ui_action(values, {"shoulder_lift.pos": True, "gripper.pos": True})

    assert inverted["shoulder_lift.pos"] == -45
    assert inverted["gripper.pos"] == 0.8
