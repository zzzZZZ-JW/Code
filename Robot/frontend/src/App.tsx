import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from "react";
import { Activity, Cable, Link2, RadioTower, RotateCcw, Settings2, SlidersHorizontal, Square, X } from "lucide-react";
import { api } from "./api";
import RobotScene, { JOINT_ORDER } from "./RobotScene";
import type { ConsoleState, JointKey, Mode, SerialPort } from "./types";

const EMPTY_JOINTS = Object.fromEntries(JOINT_ORDER.map((key) => [key, 0])) as Record<JointKey, number>;

const JOINT_LABELS: Record<JointKey, string> = {
  "shoulder_pan.pos": "肩部水平旋转",
  "shoulder_lift.pos": "肩部俯仰",
  "elbow_flex.pos": "肘部弯曲",
  "wrist_flex.pos": "腕部俯仰",
  "wrist_roll.pos": "腕部旋转",
  "gripper.pos": "夹爪开合"
};

const INITIAL_STATE: ConsoleState = {
  mode: "idle",
  ports: { leader: null, follower: null },
  connected: { leader: false, follower: false },
  calibrated: { leader: null, follower: null },
  ready: { manual: false, teleop: false },
  joints: EMPTY_JOINTS,
  leaderJoints: EMPTY_JOINTS,
  targets: EMPTY_JOINTS,
  sentTargets: EMPTY_JOINTS,
  jointLimits: [],
  inversions: Object.fromEntries(JOINT_ORDER.map((key) => [key, false])) as Record<JointKey, boolean>,
  loopHz: 0,
  lastError: null,
  usingFake: false,
  emergencyActive: false,
  readableJoints: { leader: 0, follower: 0 },
  guides: {}
};

export default function App() {
  const [state, setState] = useState<ConsoleState>(INITIAL_STATE);
  const [ports, setPorts] = useState<SerialPort[]>([]);
  const [selectedJoint, setSelectedJoint] = useState<JointKey>("shoulder_pan.pos");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [manualTargets, setManualTargets] = useState<Record<JointKey, number>>(EMPTY_JOINTS);
  const localTargetsDirtyRef = useRef(false);
  const pendingTargetsRef = useRef<Partial<Record<JointKey, number>>>({});
  const sendTimerRef = useRef<number | null>(null);

  const jointLimits = useMemo(() => new Map(state.jointLimits.map((limit) => [limit.key, limit])), [state.jointLimits]);
  const teleopActive = state.mode === "teleop";
  const controlsLocked = teleopActive || state.emergencyActive;
  const manualLocked = state.mode !== "manual" || !state.ready.manual || controlsLocked;
  const displayJoints = state.mode === "manual" ? manualTargets : state.joints;

  const run = useCallback(async (action: () => Promise<ConsoleState | void>, success?: string) => {
    setBusy(true);
    setNotice(null);
    try {
      const next = await action();
      if (next) setState(next);
      if (success) setNotice(success);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : String(error));
    } finally {
      setBusy(false);
    }
  }, []);

  const refreshPorts = useCallback(async () => {
    const response = await api.ports();
    setPorts(response.ports);
  }, []);

  useEffect(() => {
    api.state().then(setState).catch((error) => setNotice(String(error)));
    refreshPorts().catch((error) => setNotice(String(error)));

    const scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const socket = new WebSocket(`${scheme}://${window.location.host}/ws`);
    socket.onmessage = (event) => setState(JSON.parse(event.data));
    socket.onerror = () => setNotice("状态连接失败，请确认后端服务正在运行。");
    return () => socket.close();
  }, [refreshPorts]);

  useEffect(() => {
    if (state.mode !== "manual") {
      localTargetsDirtyRef.current = false;
    }
    if (!localTargetsDirtyRef.current) {
      setManualTargets(normalizeTargets(state.targets));
    }
  }, [state.mode, state.targets]);

  useEffect(() => {
    return () => {
      if (sendTimerRef.current !== null) {
        window.clearTimeout(sendTimerRef.current);
      }
    };
  }, []);

  const savePort = (role: "leader" | "follower", value: string) => {
    run(
      () =>
        api.saveSettings({
          leader_port: role === "leader" ? value : state.ports.leader,
          follower_port: role === "follower" ? value : state.ports.follower
        }),
      "串口对应已保存"
    );
  };

  const setMode = (mode: Mode) => run(() => api.setMode(mode));

  const toggleTeleop = () => {
    if (teleopActive) {
      run(() => api.setMode("manual"));
      return;
    }
    run(() => api.setMode("teleop"));
  };

  const connectCheck = () => {
    run(async () => {
      await refreshPorts();
      return api.connect(false);
    }, "连接检查完成");
  };

  const resetConsole = () => {
    run(async () => {
      await api.stop();
      await api.resetStop();
      return api.setMode("idle");
    }, "已复位到待机");
  };

  const flushPendingTargets = useCallback(() => {
    if (sendTimerRef.current !== null) {
      window.clearTimeout(sendTimerRef.current);
      sendTimerRef.current = null;
    }
    const entries = Object.entries(pendingTargetsRef.current) as [JointKey, number][];
    pendingTargetsRef.current = {};
    for (const [key, value] of entries) {
      void api.setJointTarget(key, value).catch((error) => {
        setNotice(error instanceof Error ? error.message : String(error));
      });
    }
  }, []);

  const queueTargetSend = useCallback(
    (key: JointKey, value: number) => {
      pendingTargetsRef.current[key] = value;
      if (sendTimerRef.current !== null) return;
      sendTimerRef.current = window.setTimeout(flushPendingTargets, 35);
    },
    [flushPendingTargets]
  );

  const setTarget = (key: JointKey, value: number) => {
    setSelectedJoint(key);
    setNotice(null);
    localTargetsDirtyRef.current = true;
    setManualTargets((current) => ({ ...current, [key]: value }));
    setState((current) => ({
      ...current,
      joints: { ...current.joints, [key]: value },
      targets: { ...current.targets, [key]: value }
    }));
    queueTargetSend(key, value);
  };

  return (
    <div className="simple-shell">
      <div className="app-body">
        <header className="control-bar">
          <div className="brand">
            <span className="brand-mark">SO</span>
            <div>
              <h1>SO-ARM101 控制台</h1>
              <p>本地机械臂控制</p>
            </div>
          </div>

          <section className="toolbar-block" aria-label="模式选择">
            <span className="toolbar-label">模式选择</span>
            <div className="mode-switch">
              <ModeButton active={state.mode === "idle"} onClick={() => setMode("idle")} icon={<Square />} label="待机" />
              <ModeButton
                active={state.mode === "manual"}
                disabled={!state.ready.manual || controlsLocked || busy}
                onClick={() => setMode("manual")}
                icon={<SlidersHorizontal />}
                label="控制模式"
              />
              <ModeButton
                active={state.mode === "teleop"}
                disabled={!state.ready.teleop || state.emergencyActive || busy}
                onClick={toggleTeleop}
                icon={<RadioTower />}
                label="主从联动"
              />
            </div>
          </section>

          <div className="top-actions">
            <button className="button primary" disabled={busy || teleopActive} onClick={connectCheck}>
              <Cable size={18} />
              <span>连接检查</span>
            </button>
            <button className="button" disabled={busy || teleopActive} onClick={() => setSettingsOpen(true)}>
              <Settings2 size={18} />
              <span>设置</span>
            </button>
            <button className="button secondary" disabled={busy} onClick={resetConsole}>
              <RotateCcw size={18} />
              <span>复位</span>
            </button>
          </div>
        </header>

        <main className="main-grid">
          <section className="panel status-panel" aria-label="运行状态">
            <SectionTitle icon={<Link2 size={18} />} title="运行状态" />
            <div className="status-list">
              <StatusRow label="主臂状态" value={deviceText(state.connected.leader, state.calibrated.leader, state.readableJoints.leader)} />
              <StatusRow label="从臂状态" value={deviceText(state.connected.follower, state.calibrated.follower, state.readableJoints.follower)} />
              <StatusRow label="当前模式" value={state.usingFake ? `${modeText(state.mode)} / 模拟` : modeText(state.mode)} />
              <StatusRow label="控制对象" value="从臂" />
              <StatusRow label="循环频率" value={`${state.loopHz.toFixed(1)} Hz`} />
            </div>

            {(state.lastError || notice) && <div className="notice">{translateNotice(state.lastError || notice)}</div>}
          </section>

          <section className="panel state-panel" aria-label="机械臂状态视图">
            <SectionTitle icon={<Activity size={18} />} title="机械臂状态视图" />
            <div className="robot-stage">
              <RobotScene joints={displayJoints} selectedJoint={selectedJoint} />
              <div className="joint-rail" aria-label="关节当前状态">
                {JOINT_ORDER.map((key) => (
                  <button
                    key={key}
                    className={`joint-chip ${selectedJoint === key ? "selected" : ""}`}
                    onClick={() => setSelectedJoint(key)}
                    title={key}
                  >
                    <span>{JOINT_LABELS[key]}</span>
                    <strong>{formatJointValue(displayJoints[key], key)}</strong>
                  </button>
                ))}
              </div>
            </div>
          </section>

          <section className={`panel sliders-panel ${controlsLocked ? "controls-locked" : ""}`} aria-label="关节控制滑块">
            <SectionTitle icon={<SlidersHorizontal size={18} />} title="从臂关节控制" />
            {teleopActive && <div className="teleop-note">主从联动中，再次点击“主从联动”退出</div>}
            <div className="slider-list">
              {JOINT_ORDER.map((key) => {
                const limit = jointLimits.get(key);
                const current = displayJoints[key] ?? 0;
                const target = manualTargets[key] ?? current;
                return (
                  <label className={`slider-row ${selectedJoint === key ? "selected" : ""}`} key={key}>
                    <span className="slider-name">{JOINT_LABELS[key]}</span>
                    <span className="slider-current">设定 {formatJointValue(current, key)}</span>
                    <input
                      className="slider"
                      type="range"
                      min={limit?.min_value ?? 0}
                      max={limit?.max_value ?? 1}
                      step={limit?.step ?? 0.01}
                      value={target}
                      disabled={manualLocked || busy || !limit}
                      onFocus={() => setSelectedJoint(key)}
                      onChange={(event) => setTarget(key, Number(event.target.value))}
                      onPointerUp={flushPendingTargets}
                      onTouchEnd={flushPendingTargets}
                      onKeyUp={flushPendingTargets}
                    />
                    <span className="slider-target">发送 {formatJointValue(target, key)}</span>
                  </label>
                );
              })}
            </div>
          </section>
        </main>
      </div>

      {settingsOpen && (
        <div className="settings-layer" role="dialog" aria-modal="true" aria-label="设置">
          <div className="settings-panel">
            <div className="settings-head">
              <div>
                <h2>设置</h2>
                <p>串口与机械臂对应</p>
              </div>
              <button className="icon-button" onClick={() => setSettingsOpen(false)} title="关闭设置">
                <X size={18} />
              </button>
            </div>
            <div className="port-grid">
              <label className="field">
                <span>主臂串口</span>
                <select value={state.ports.leader ?? ""} disabled={busy} onChange={(event) => savePort("leader", event.target.value)}>
                  <option value="">选择端口</option>
                  {ports.map((port) => (
                    <option key={`leader-${port.device}`} value={port.device}>
                      {port.device}
                    </option>
                  ))}
                </select>
              </label>
              <label className="field">
                <span>从臂串口</span>
                <select value={state.ports.follower ?? ""} disabled={busy} onChange={(event) => savePort("follower", event.target.value)}>
                  <option value="">选择端口</option>
                  {ports.map((port) => (
                    <option key={`follower-${port.device}`} value={port.device}>
                      {port.device}
                    </option>
                  ))}
                </select>
              </label>
            </div>
            <button className="button primary wide" disabled={busy} onClick={() => run(() => refreshPorts(), "端口已刷新")}>
              <Cable size={18} />
              <span>刷新串口</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

function ModeButton({
  active,
  disabled,
  onClick,
  icon,
  label
}: {
  active: boolean;
  disabled?: boolean;
  onClick: () => void;
  icon: ReactNode;
  label: string;
}) {
  return (
    <button className={`mode-button ${active ? "active" : ""}`} disabled={disabled} onClick={onClick}>
      {icon}
      <span>{label}</span>
    </button>
  );
}

function SectionTitle({ icon, title }: { icon: ReactNode; title: string }) {
  return (
    <div className="section-title">
      {icon}
      <h2>{title}</h2>
    </div>
  );
}

function StatusRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="status-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function deviceText(connected: boolean, calibrated: boolean | null, readable: number) {
  if (!connected) return "未连接";
  if (calibrated === false) return `需校准 / ${readable}`;
  return `就绪 / ${readable}`;
}

function normalizeTargets(values: Partial<Record<JointKey, number>> | null | undefined) {
  return Object.fromEntries(JOINT_ORDER.map((key) => [key, Number(values?.[key] ?? 0)])) as Record<JointKey, number>;
}

function formatJointValue(value: number | undefined, key: JointKey) {
  const safe = Number(value ?? 0);
  if (key === "gripper.pos") return safe.toFixed(2);
  return `${safe.toFixed(1)}度`;
}

function modeText(mode: Mode) {
  if (mode === "manual") return "控制模式";
  if (mode === "teleop") return "主从联动";
  return "待机";
}

function translateNotice(message: string | null) {
  if (!message) return "";
  return message
    .replace("Leader and follower ports are required for real hardware mode.", "真实硬件模式需要同时选择主臂和从臂端口。")
    .replace("Emergency stop is active. Reset it before enabling motion.", "急停已激活，请先复位再启用运动。")
    .replace("Follower must be connected and calibrated before manual control.", "进入控制模式前，从臂必须已连接并完成校准。")
    .replace("Leader and follower must be connected and calibrated before teleoperation.", "进入主从联动前，主臂和从臂都必须已连接并完成校准。")
    .replace("Joint targets can only be changed in manual mode.", "只能在控制模式下修改关节目标。");
}
