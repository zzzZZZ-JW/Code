from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from uuid import uuid4


@dataclass(frozen=True)
class SerialPort:
    device: str
    name: str
    description: str = ""
    hwid: str = ""
    serial_number: str | None = None


class PortIdentifier:
    def __init__(self) -> None:
        self._snapshots: dict[str, set[str]] = {}

    def start(self) -> dict[str, object]:
        snapshot_id = str(uuid4())
        ports = list_serial_ports()
        self._snapshots[snapshot_id] = {port.device for port in ports}
        return {"snapshot_id": snapshot_id, "ports": [asdict(port) for port in ports]}

    def finish(self, snapshot_id: str) -> dict[str, object]:
        before = self._snapshots.pop(snapshot_id, set())
        after_ports = list_serial_ports()
        after = {port.device for port in after_ports}
        removed = sorted(before - after)
        added = sorted(after - before)
        return {
            "removed": removed,
            "added": added,
            "identified_port": removed[0] if len(removed) == 1 else None,
            "ports": [asdict(port) for port in after_ports],
        }


def list_serial_ports() -> list[SerialPort]:
    try:
        from serial.tools import list_ports

        ports = []
        for port in list_ports.comports():
            ports.append(
                SerialPort(
                    device=port.device,
                    name=port.name or Path(port.device).name,
                    description=port.description or "",
                    hwid=port.hwid or "",
                    serial_number=getattr(port, "serial_number", None),
                )
            )
        return sorted(ports, key=lambda item: item.device)
    except Exception:
        devices = sorted({str(path) for pattern in ("/dev/cu.*", "/dev/tty.*") for path in Path("/").glob(pattern[1:])})
        return [
            SerialPort(device=device, name=Path(device).name, description="Serial port", hwid="")
            for device in devices
        ]

