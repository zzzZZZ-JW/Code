import math
import time
import roslibpy

# 导入 LeRobot 相关的库
from lerobot.robots.so_follower.so_follower import SO101Follower
from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig

class SO101RoslibpyBridge:
    def __init__(self):
        self.motor_names = [
            "shoulder_pan.pos",
            "shoulder_lift.pos",
            "elbow_flex.pos",
            "wrist_flex.pos",
            "wrist_roll.pos",
            "gripper.pos"
        ]
        self.angle_limit = {"min": -90.0, "max": 90.0}
        
        self.robot = None
        self.init_robot()

        # 这里的 localhost:9090 会自动穿透连接到 WSL 内部的 rosbridge
        self.client = roslibpy.Ros(host='localhost', port=9090)
        
        # 订阅你在 Isaac Sim 中设定的动作指令话题 (/sim_joint_commands)
        self.listener = roslibpy.Topic(self.client, '/sim_joint_commands', 'sensor_msgs/JointState')
        self.listener.subscribe(self.joint_command_callback)

    def init_robot(self):
        print(">>> 正在连接 COM4 从臂，请稍候...")
        try:
            config = SOFollowerRobotConfig(port="COM4")
            self.robot = SO101Follower(config)
            self.robot.connect()
            print("✅ 从臂连接成功！底层校准已加载。")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            self.robot = None

    def joint_command_callback(self, msg):
        if self.robot is None:
            return

        action_dict = {}
        # 通过 WebSocket 传过来的 msg 是标准的 Python 字典，对应 JSON 结构
        names = msg.get('name', [])
        positions = msg.get('position', [])

        for i, motor_name in enumerate(self.motor_names):
            if i < len(positions):
                val = positions[i]
                if motor_name == "gripper.pos":
                    action_dict[motor_name] = max(0.0, min(100.0, val * 100.0))
                else:
                    angle_deg = val * (180.0 / math.pi)
                    action_dict[motor_name] = max(self.angle_limit["min"], min(self.angle_limit["max"], angle_deg))

        try:
            self.robot.send_action(action_dict)
        except Exception as e:
            print(f"⚠️ 发送指令异常: {e}")

    def run(self):
        print(">>> 正在尝试连接 WSL 的 ROS2 桥接服务...")
        self.client.run()
        if self.client.is_connected:
            print("✅ WebSocket 通信节点已就绪，正在持续监听 Isaac Sim 指令...")
            try:
                # 保持主线程存活
                while self.client.is_connected:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                self.shutdown()
        else:
            print("❌ 无法连接到 WSL，请确保已在 WSL 中运行 rosbridge_websocket")

    def shutdown(self):
        print("\n>>> 正在关闭网络连接并释放机械臂扭矩...")
        if self.robot is not None:
            try:
                self.robot.disconnect()
            except:
                pass
        self.client.terminate()

if __name__ == '__main__':
    bridge = SO101RoslibpyBridge()
    bridge.run()