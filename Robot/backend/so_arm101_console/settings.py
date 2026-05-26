from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .joints import JOINT_KEYS


class AppSettings(BaseModel):
    leader_port: str | None = None
    follower_port: str | None = None
    inversions: dict[str, bool] = Field(default_factory=lambda: {key: False for key in JOINT_KEYS})


class SettingsStore:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> AppSettings:
        if not self.path.exists():
            return AppSettings()
        try:
            data: dict[str, Any] = json.loads(self.path.read_text(encoding="utf-8"))
            settings = AppSettings.model_validate(data)
        except Exception:
            return AppSettings()
        settings.inversions = {key: bool(settings.inversions.get(key, False)) for key in JOINT_KEYS}
        return settings

    def save(self, settings: AppSettings) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(settings.model_dump_json(indent=2), encoding="utf-8")

