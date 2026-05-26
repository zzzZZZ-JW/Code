import math
import socket
import json
import time
from lerobot.robots.so_follower.so_follower import SO101Follower
from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig

class SO101UDPBridge:
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

        # 在 Windows 本地建立接收站
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", 9090))

    def init_robot(self):
        print(">>> 正在连接 COM4 从臂，请稍候...")
        try:
            config = SOFollowerRobotConfig(port="COM4")
            self.robot = SO101Follower(config)
            self.robot.connect()
            print(">>> 从臂连接成功！底层校准已加载。")
        except Exception as e:
            print(f">>> 连接失败: {e}")
            self.robot = None

    def run(self):
        print(">>> 本地 UDP 通信节点已就绪，正在持续监听 Isaac Sim 指令...")
        try:
            while True:
                # 接收来自 Isaac Sim 的数据包
                data, addr = self.sock.recvfrom(1024)
                msg = json.loads(data.decode('utf-8'))
                self.process_command(msg)
        except KeyboardInterrupt:
            self.shutdown()

    def process_command(self, msg):
        if self.robot is None:
            return

        action_dict = {}
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
            print(f">>> 发送指令异常: {e}")

    def shutdown(self):
        print("\n>>> 正在关闭网络连接并释放机械臂扭矩...")
        if self.robot is not None:
            try:
                self.robot.disconnect()
            except:
                pass
        self.sock.close()

if __name__ == '__main__':
    bridge = SO101UDPBridge()
    bridge.run()