# SO-ARM101 本地控制台

这是一个面向两只 SO-ARM101/SO-101 机械臂的本地网页控制台：

- 后端：FastAPI，负责串口识别、LeRobot/Feetech 通信、限幅、急停、自由控制和主从联动循环。
- 前端：React + Three.js，负责 3D 姿态显示、关节点击、滑杆控制、主从映射和硬件向导。
- 离线验证：未安装 LeRobot 或未接机械臂时，可以用 Fake device 先跑 UI 和控制逻辑。

## 当前硬件前置条件

本机已能看到两个 USB 串口：

```bash
/dev/cu.usbmodem5B140313231
/dev/cu.usbmodem5B141151161
```

程序不会假设哪一个是主臂或从臂。首次运行时在页面里使用 `识别主臂`、`识别从臂`，按提示拔掉对应机械臂 USB 后完成识别。

## 安装

推荐使用 Python 3.12。LeRobot 官方安装说明也以 Python 3.12 为目标。

```bash
cd /Users/zhangjiawei/Code/Robot
uv python install 3.12
uv sync --extra hardware --group dev
npm install --prefix frontend
```

如果只是先看 UI，可以暂时不装硬件 extra：

```bash
uv sync --group dev
npm install --prefix frontend
```

## 运行

开两个终端：

```bash
cd /Users/zhangjiawei/Code/Robot
uv run uvicorn so_arm101_console.main:app --app-dir backend --reload --host 127.0.0.1 --port 8000
```

```bash
cd /Users/zhangjiawei/Code/Robot
npm run dev --prefix frontend
```

打开：

```text
http://127.0.0.1:5173
```

前端构建后，FastAPI 也可以直接服务静态页面：

```bash
npm run build --prefix frontend
uv run uvicorn so_arm101_console.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

然后打开 `http://127.0.0.1:8000`。

## 硬件流程

页面内会显示与当前端口匹配的命令。核心命令如下：

```bash
lerobot-find-port
lerobot-setup-motors --robot.type=so101_follower --robot.port=<follower-port>
lerobot-setup-motors --teleop.type=so101_leader --teleop.port=<leader-port>
lerobot-calibrate --robot.type=so101_follower --robot.port=<follower-port> --robot.id=so101_follower_slave
lerobot-calibrate --teleop.type=so101_leader --teleop.port=<leader-port> --teleop.id=so101_leader_main
```

使用固定 id 可以复用 LeRobot 校准文件。

## 安全行为

- 未连接或未校准时，页面不能进入自由控制或主从联动。
- 自由控制只向从臂发送目标；主从联动会锁定手动控制并持续读取主臂。
- 所有关节目标都会按 SO-ARM101 角度范围限幅。
- 每个控制周期只允许有限幅度变化，避免一次性跳到远距离目标。
- 急停会立刻切回 `Idle`，停止发送新目标，并尝试关闭从臂 torque。

## 测试

```bash
uv run pytest
npm run build --prefix frontend
```

