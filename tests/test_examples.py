from pathlib import Path

import yaml

from goodinfo_screener.presets import Preset, validate_goodinfo_url


def test_high_margin_example_is_valid_preset_yaml() -> None:
    path = Path("examples/high-margin.yml")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    preset = Preset.model_validate(data["presets"]["high-margin"])

    assert preset.source == "goodinfo"
    validate_goodinfo_url(preset.url)
