from so_arm101_console.ports import PortIdentifier, SerialPort


def test_port_identifier_detects_single_removed_port(monkeypatch):
    snapshots = [
        [SerialPort("/dev/tty.a", "tty.a"), SerialPort("/dev/tty.b", "tty.b")],
        [SerialPort("/dev/tty.a", "tty.a")],
    ]

    monkeypatch.setattr("so_arm101_console.ports.list_serial_ports", lambda: snapshots.pop(0))

    identifier = PortIdentifier()
    started = identifier.start()
    finished = identifier.finish(started["snapshot_id"])

    assert finished["identified_port"] == "/dev/tty.b"
    assert finished["removed"] == ["/dev/tty.b"]

