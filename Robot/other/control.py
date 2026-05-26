import tkinter as tk
from tkinter import ttk
import time
import threading

# 导入 LeRobot 相关的库
from lerobot.robots.so_follower.so_follower import SO101Follower
from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig

class RobotArmController(tk.Tk):
    def __init__(self):
        super().__init__()

        # 窗口基础设置
        self.title("🦾 SO-101 现代交互控制台")
        self.geometry("700x750")
        self.resizable(False, False)
        self.configure(bg="#F3F4F6") # 现代浅灰背景
        
        # 映射 LeRobot 的电机名称
        self.motor_names = [
            "shoulder_pan.pos",
            "shoulder_lift.pos",
            "elbow_flex.pos",
            "wrist_flex.pos",
            "wrist_roll.pos",
            "gripper.pos"
        ]

        # 舵机配置，增加键盘快捷键提示和映射
        self.servos = [
            {"id": 1, "name": "底座 (Base)", "angle": 0, "min": -90, "max": 90, "keys": ("q", "a"), "keys_label": "[Q/A]"},
            {"id": 2, "name": "大臂 (Shoulder)", "angle": 0, "min": -90, "max": 90, "keys": ("w", "s"), "keys_label": "[W/S]"},
            {"id": 3, "name": "小臂 (Elbow)", "angle": 0, "min": -90, "max": 90, "keys": ("e", "d"), "keys_label": "[E/D]"},
            {"id": 4, "name": "腕部俯仰 (Pitch)", "angle": 0, "min": -90, "max": 90, "keys": ("r", "f"), "keys_label": "[R/F]"},
            {"id": 5, "name": "腕部旋转 (Roll)", "angle": 0, "min": -90, "max": 90, "keys": ("t", "g"), "keys_label": "[T/G]"},
            {"id": 6, "name": "夹爪 (Gripper)", "angle": 50, "min": 0, "max": 100, "keys": ("y", "h"), "keys_label": "[Y/H]"}
        ]
        
        # 构建键盘映射字典 {键位: (舵机索引, 方向增量)}
        self.key_map = {}
        for i, servo in enumerate(self.servos):
            self.key_map[servo["keys"][0]] = (i, 2)  # 正向步进2度
            self.key_map[servo["keys"][1]] = (i, -2) # 反向步进2度
        
        # 动作字典
        self.current_action = {name: 0.0 for name in self.motor_names}
        self.current_action["gripper.pos"] = 50.0

        self.setup_ui()
        
        # 绑定全局键盘事件
        self.bind("<KeyPress>", self.on_key_press)
        # 窗口关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 启动硬件连接
        self.init_robot()

    def setup_ui(self):
        # 现代 UI 样式配置
        style = ttk.Style(self)
        style.theme_use('clam') 
        style.configure("TLabel", background="#FFFFFF", font=("Microsoft YaHei", 10))
        style.configure("Card.TFrame", background="#FFFFFF")
        style.configure("Header.TLabel", background="#FFFFFF", font=("Microsoft YaHei", 12, "bold"), foreground="#1F2937")
        style.configure("Info.TLabel", background="#E5E7EB", font=("Microsoft YaHei", 9), foreground="#4B5563")

        # --- 顶部：说明与状态面板 ---
        header_frame = tk.Frame(self, bg="#E5E7EB", padx=10, pady=10)
        header_frame.pack(fill="x")
        ttk.Label(header_frame, text="💡 控制方式：1. 鼠标拖动滑块  2. 鼠标悬浮滑块并滚动滚轮  3. 键盘按键对应操作", style="Info.TLabel").pack()

        # --- 中间：控制卡片 ---
        self.control_frame = ttk.Frame(self, style="Card.TFrame")
        self.control_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ttk.Label(self.control_frame, text="关节状态控制", style="Header.TLabel").pack(pady=(15, 5))
        
        self.sliders = []
        self.angle_vars = []

        for i, servo in enumerate(self.servos):
            row_frame = ttk.Frame(self.control_frame, style="Card.TFrame")
            row_frame.pack(fill="x", pady=10, padx=20)

            # 快捷键提示
            ttk.Label(row_frame, text=servo['keys_label'], width=6, foreground="#3B82F6").pack(side="left")
            # 舵机名称标签
            ttk.Label(row_frame, text=f"{servo['name']}", width=18).pack(side="left")

            var = tk.IntVar(value=servo['angle'])
            self.angle_vars.append(var)

            # 数值显示
            unit = "%" if i == 5 else "°"
            angle_label = ttk.Label(row_frame, textvariable=var, width=4, anchor="e")
            angle_label.pack(side="right")
            ttk.Label(row_frame, text=unit).pack(side="right", padx=(0, 10))

            # 滑块控件
            slider = ttk.Scale(
                row_frame, 
                from_=servo['min'], 
                to=servo['max'], 
                orient="horizontal",
                variable=var,
                command=lambda val, idx=i: self.on_slider_drag(idx, val)
            )
            slider.pack(side="left", fill="x", expand=True, padx=15)
            self.sliders.append(slider)
            
            # 为当前行和滑块绑定鼠标滚轮事件 (Windows 使用 <MouseWheel>)
            slider.bind("<MouseWheel>", lambda event, idx=i: self.on_mouse_wheel(event, idx))
            row_frame.bind("<MouseWheel>", lambda event, idx=i: self.on_mouse_wheel(event, idx))

        # 居中复位按钮
        self.reset_btn = tk.Button(self.control_frame, text="🔄 一键居中复位", bg="#EF4444", fg="white", 
                                   font=("Microsoft YaHei", 10, "bold"), relief="flat", padx=20, pady=5, 
                                   cursor="hand2", command=self.reset_servos)
        self.reset_btn.pack(pady=20)

        # --- 底部：日志输出 ---
        log_container = ttk.Frame(self, style="Card.TFrame")
        log_container.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(log_container, text="系统日志", style="Header.TLabel").pack(anchor="w", padx=15, pady=(10,0))
        self.log_textbox = tk.Text(log_container, height=6, bg="#F9FAFB", fg="#374151", font=("Consolas", 9), relief="flat")
        self.log_textbox.pack(pady=10, padx=15, fill="x")
        self.log_textbox.insert("1.0", "界面初始化完成，可以开始控制。\n")
        self.log_textbox.configure(state="disabled")

    def log(self, message):
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")
        self.update()

    def init_robot(self):
        self.log(">>> 正在连接 COM4 从臂，请稍候...")
        try:
            config = SOFollowerRobotConfig(port="COM4")
            self.robot = SO101Follower(config)
            self.robot.connect()
            
            # 同步初始真实位置
            obs = self.robot.get_observation()
            for i, name in enumerate(self.motor_names):
                real_pos = obs.get(name, 0.0)
                self.update_joint(i, real_pos, send=False)
                
            self.log("✅ 从臂连接成功！底层校准已加载。")
        except Exception as e:
            self.log(f"❌ 连接失败: {e}")
            self.robot = None

    def update_joint(self, idx, new_value, send=True):
        """核心关节更新逻辑（处理所有输入源的数据）"""
        # 限制在最小值和最大值之间
        new_value = max(self.servos[idx]['min'], min(self.servos[idx]['max'], int(float(new_value))))
        
        if new_value != self.servos[idx]['angle']:
            self.servos[idx]['angle'] = new_value
            self.angle_vars[idx].set(new_value)
            
            motor_name = self.motor_names[idx]
            self.current_action[motor_name] = float(new_value)
            
            if send:
                self.send_command()

    def on_slider_drag(self, idx, value):
        """响应鼠标拖拽"""
        self.update_joint(idx, value)

    def on_mouse_wheel(self, event, idx):
        """响应鼠标滚轮"""
        # event.delta 在 Windows 上滚轮向上为正(通常120)，向下为负
        step = 2 if event.delta > 0 else -2
        current = self.servos[idx]['angle']
        self.update_joint(idx, current + step)

    def on_key_press(self, event):
        """响应键盘按键"""
        char = event.char.lower()
        if char in self.key_map:
            idx, step = self.key_map[char]
            current = self.servos[idx]['angle']
            self.update_joint(idx, current + step)

    def reset_servos(self):
        self.log(">>> 正在执行全部复位指令 (居中)...")
        for i, servo in enumerate(self.servos):
            default_angle = 50 if i == 5 else 0
            self.update_joint(i, default_angle, send=False)
        self.send_command()

    def send_command(self):
        if hasattr(self, 'robot') and self.robot is not None:
            try:
                self.robot.send_action(self.current_action)
            except Exception as e:
                self.log(f"⚠️ 发送指令异常: {e}")

    def on_closing(self):
        self.log(">>> 正在释放机械臂扭矩并断开连接...")
        if hasattr(self, 'robot') and self.robot is not None:
            try:
                self.robot.disconnect()
            except:
                pass
        self.destroy()

if __name__ == "__main__":
    app = RobotArmController()
    app.mainloop()