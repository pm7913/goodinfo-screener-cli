"""Local preset storage for Goodinfo screener URLs."""

from __future__ import annotations

import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse

import yaml
from pydantic import BaseModel, Field

APP_DIR_NAME = "goodinfo-screener-cli"
PRESET_FILE_NAME = "presets.yml"
CONFIG_DIR_ENV = "GOODINFO_SCREENER_CONFIG_DIR"

PRESET_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


class PresetError(Exception):
    """Base error for preset operations."""


class InvalidPresetNameError(PresetError):
    """Raised when a preset name does not match the expected format."""


class InvalidGoodinfoUrlError(PresetError):
    """Raised when a URL is not a supported Goodinfo screener URL."""


class PresetExistsError(PresetError):
    """Raised when adding a preset that already exists without force."""


class PresetNotFoundError(PresetError):
    """Raised when a requested preset does not exist."""


class BrowserSettings(BaseModel):
    """Browser settings stored with each preset."""

    headless: bool = True
    timeout_ms: int = Field(default=30000, gt=0)


class OutputSettings(BaseModel):
    """Default output settings stored with each preset."""

    format: Literal["table"] = "table"


class Preset(BaseModel):
    """A saved Goodinfo screener preset."""

    source: Literal["goodinfo"] = "goodinfo"
    url: str
    created_at: datetime
    browser: BrowserSettings = Field(default_factory=BrowserSettings)
    output: OutputSettings = Field(default_factory=OutputSettings)


def config_dir() -> Path:
    """Return the config directory for preset storage."""
    override = os.environ.get(CONFIG_DIR_ENV)
    if override:
        return Path(override).expanduser()
    return Path.home() / ".config" / APP_DIR_NAME


def preset_file_path(base_dir: Path | None = None) -> Path:
    """Return the preset YAML file path."""
    return (base_dir or config_dir()) / PRESET_FILE_NAME


def init_store(base_dir: Path | None = None) -> Path:
    """Create the preset directory and file when missing."""
    path = preset_file_path(base_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("presets: {}\n", encoding="utf-8")
    return path


def validate_preset_name(name: str) -> None:
    """Validate a preset name."""
    if not PRESET_NAME_RE.fullmatch(name):
        raise InvalidPresetNameError(
            "Preset names must start with a letter or number and contain only "
            "letters, numbers, underscores, or hyphens."
        )


def validate_goodinfo_url(url: str) -> None:
    """Validate that a URL targets the supported Goodinfo stock list page."""
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise InvalidGoodinfoUrlError("Goodinfo URLs must use https.")
    if parsed.netloc.lower() != "goodinfo.tw":
        raise InvalidGoodinfoUrlError("URL host must be goodinfo.tw.")
    if parsed.path != "/tw/StockList.asp":
        raise InvalidGoodinfoUrlError("URL path must be /tw/StockList.asp.")


def load_presets(base_dir: Path | None = None) -> dict[str, Preset]:
    """Load presets from YAML storage."""
    path = preset_file_path(base_dir)
    if not path.exists():
        return {}

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    raw_presets = raw.get("presets") or {}
    return {name: Preset.model_validate(value) for name, value in raw_presets.items()}


def save_presets(presets: dict[str, Preset], base_dir: Path | None = None) -> Path:
    """Persist presets to YAML storage."""
    path = init_store(base_dir)
    payload = {
        "presets": {
            name: preset.model_dump(mode="json", exclude_none=True)
            for name, preset in presets.items()
        }
    }
    path.write_text(yaml.safe_dump(payload, sort_keys=True, allow_unicode=True), encoding="utf-8")
    return path


def add_preset(
    name: str,
    url: str,
    *,
    force: bool = False,
    base_dir: Path | None = None,
) -> Preset:
    """Add or update a preset."""
    validate_preset_name(name)
    validate_goodinfo_url(url)

    presets = load_presets(base_dir)
    if name in presets and not force:
        raise PresetExistsError(f"Preset `{name}` already exists. Use --force to overwrite it.")

    preset = Preset(url=url, created_at=datetime.now(UTC))
    presets[name] = preset
    save_presets(presets, base_dir)
    return preset


def remove_preset(name: str, *, base_dir: Path | None = None) -> Preset:
    """Remove and return a preset."""
    validate_preset_name(name)
    presets = load_presets(base_dir)
    if name not in presets:
        raise PresetNotFoundError(f"Preset `{name}` does not exist.")

    removed = presets.pop(name)
    save_presets(presets, base_dir)
    return removed
