import asyncio

from so_arm101_console.controller import RobotController


def test_fake_controller_manual_mode_is_safe(tmp_path):
    async def scenario():
        controller = RobotController(tmp_path)
        await controller.start()
        try:
            state = await controller.connect(use_fake=True)
            assert state["ready"]["teleop"] is True
            assert state["usingFake"] is True

            await controller.set_mode("manual")
            await controller.set_joint_target("shoulder_pan.pos", 170)
            await asyncio.sleep(0.08)
            state = await controller.snapshot()

            assert state["targets"]["shoulder_pan.pos"] == 90
            assert state["joints"]["shoulder_pan.pos"] == 90
            assert state["sentTargets"]["shoulder_pan.pos"] == 90

            await controller.emergency_stop()
            stopped = await controller.snapshot()
            assert stopped["mode"] == "idle"
            assert stopped["emergencyActive"] is True
        finally:
            await controller.stop()

    asyncio.run(scenario())
