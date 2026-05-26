export type Mode = "idle" | "manual" | "teleop";

export type JointKey =
  | "shoulder_pan.pos"
  | "shoulder_lift.pos"
  | "elbow_flex.pos"
  | "wrist_flex.pos"
  | "wrist_roll.pos"
  | "gripper.pos";

export interface JointLimit {
  key: JointKey;
  label: string;
  min_value: number;
  max_value: number;
  step: number;
  max_delta_per_tick: number;
  unit: string;
}

export interface SerialPort {
  device: string;
  name: string;
  description: string;
  hwid: string;
  serial_number?: string | null;
}

export interface ConsoleState {
  mode: Mode;
  ports: {
    leader: string | null;
    follower: string | null;
  };
  connected: {
    leader: boolean;
    follower: boolean;
  };
  calibrated: {
    leader: boolean | null;
    follower: boolean | null;
  };
  ready: {
    manual: boolean;
    teleop: boolean;
  };
  joints: Record<JointKey, number>;
  leaderJoints: Record<JointKey, number>;
  targets: Record<JointKey, number>;
  sentTargets: Record<JointKey, number>;
  jointLimits: JointLimit[];
  inversions: Record<JointKey, boolean>;
  loopHz: number;
  lastError: string | null;
  usingFake: boolean;
  emergencyActive: boolean;
  readableJoints: {
    leader: number;
    follower: number;
  };
  guides: Record<string, string[]>;
}

export interface PortIdentifyStart {
  snapshot_id: string;
  ports: SerialPort[];
}

export interface PortIdentifyFinish {
  removed: string[];
  added: string[];
  identified_port: string | null;
  ports: SerialPort[];
}

