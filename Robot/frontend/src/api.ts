import type { ConsoleState, JointKey, Mode, PortIdentifyFinish, PortIdentifyStart, SerialPort } from "./types";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {})
    },
    ...init
  });
  if (!response.ok) {
    let message = response.statusText;
    try {
      const body = await response.json();
      message = body.detail ?? message;
    } catch {
      // Keep status text.
    }
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export const api = {
  state: () => request<ConsoleState>("/api/state"),
  ports: () => request<{ ports: SerialPort[] }>("/api/ports"),
  guides: () => request<Record<string, string[]>>("/api/guides"),
  saveSettings: (body: { leader_port?: string | null; follower_port?: string | null; inversions?: Partial<Record<JointKey, boolean>> }) =>
    request<ConsoleState>("/api/settings", { method: "PUT", body: JSON.stringify(body) }),
  connect: (useFake: boolean) =>
    request<ConsoleState>("/api/connect", { method: "POST", body: JSON.stringify({ use_fake: useFake }) }),
  disconnect: () => request<ConsoleState>("/api/disconnect", { method: "POST" }),
  stop: () => request<ConsoleState>("/api/stop", { method: "POST" }),
  resetStop: () => request<ConsoleState>("/api/stop/reset", { method: "POST" }),
  setMode: (mode: Mode) => request<ConsoleState>("/api/mode", { method: "POST", body: JSON.stringify({ mode }) }),
  setJointTarget: (key: JointKey, value: number) =>
    request<ConsoleState>(`/api/joints/${encodeURIComponent(key)}/target`, {
      method: "POST",
      body: JSON.stringify({ value })
    }),
  identifyStart: () => request<PortIdentifyStart>("/api/ports/identify/start", { method: "POST" }),
  identifyFinish: (snapshotId: string) =>
    request<PortIdentifyFinish>("/api/ports/identify/finish", {
      method: "POST",
      body: JSON.stringify({ snapshot_id: snapshotId })
    })
};

