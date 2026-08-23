# config_loader.py
# Reads settings.cfg for KM-Waechter runtime configuration.

from typing import Any

SETTINGS_FILE: str = "settings.cfg"

KNOWN_KEYS: list[str] = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Load key=value settings from a cfg file, ignoring comments and unknown keys."""
    if path is None:
        path = SETTINGS_FILE
    settings: dict[str, str] = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return an integer setting, falling back if missing or unparseable."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Return a string setting, falling back if missing."""
    return settings.get(key, fallback)
