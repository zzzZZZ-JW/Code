#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import sys
import termios
import tty
import select

class JointKeyboardControl(Node):
    def __init__(self):
        super().__init__('joint_keyboard_control')
        self.publisher_ = self.create_publisher(JointState, '/joint_command', 10)

        # 關節名稱（與 /joint_states 一致）
        self.joint_names = [
            'shoulder_pan',
            'shoulder_lift',
            'elbow_flex',
            'wrist_flex',
            'wrist_roll',
            'gripper'
        ]

        # 當前關節位置（初始為0）
        self.joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        # 當前選中關節索引（預設第一個）
        self.selected_joint = 0

        # 關節調整步長
        self.step_size = 0.01

        # 保存終端設定
        self.old_settings = termios.tcgetattr(sys.stdin)

        # 操作提示
        self.print_instructions()

    def print_instructions(self):
        print("\n=== 機械臂鍵盤控制 ===")
        print("1-6: 選擇關節")
        print("a/d: 調整關節位置（a=減小, d=增大）")
        print("q: 退出程式")
        print("當前關節:", self.joint_names[self.selected_joint])
        print("當前位置:", self.joint_positions[self.selected_joint])

    def get_key(self):
        # 非阻塞讀取鍵盤輸入
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return None

    def run(self):
        try:
            # 設置終端為非阻塞模式
            tty.setcbreak(sys.stdin.fileno())

            while rclpy.ok():
                key = self.get_key()
                if key is not None:
                    # 選擇關節（1-6）
                    if key in ['1', '2', '3', '4', '5', '6']:
                        self.selected_joint = int(key) - 1
                        print("\n當前關節:", self.joint_names[self.selected_joint])
                        print("當前位置:", self.joint_positions[self.selected_joint])

                    # 調整關節位置（a=減小, d=增大）
                    elif key == 'a':
                        self.joint_positions[self.selected_joint] -= self.step_size
                        self.publish_joint_command()
                        print("位置 -:", self.joint_positions[self.selected_joint])

                    elif key == 'd':
                        self.joint_positions[self.selected_joint] += self.step_size
                        self.publish_joint_command()
                        print("位置 +:", self.joint_positions[self.selected_joint])

                    # 退出程式（q）
                    elif key == 'q':
                        print("\n退出程式...")
                        break

                # 短暫休眠，避免CPU過高
                rclpy.spin_once(self, timeout_sec=0.01)

        finally:
            # 恢復終端設定
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def publish_joint_command(self):
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names
        msg.position = self.joint_positions
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    joint_keyboard_control = JointKeyboardControl()

    try:
        joint_keyboard_control.run()
    except KeyboardInterrupt:
        pass
    finally:
        joint_keyboard_control.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()