from pathlib import Path

import pytest
import yaml

from goodinfo_screener.presets import (
    InvalidGoodinfoUrlError,
    InvalidPresetNameError,
    PresetExistsError,
    PresetNotFoundError,
    add_preset,
    init_store,
    load_presets,
    remove_preset,
    validate_goodinfo_url,
    validate_preset_name,
)

GOODINFO_URL = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=test"


def test_init_store_creates_yaml_file(tmp_path: Path) -> None:
    path = init_store(tmp_path)

    assert path.exists()
    assert yaml.safe_load(path.read_text(encoding="utf-8")) == {"presets": {}}


def test_add_load_and_remove_preset(tmp_path: Path) -> None:
    preset = add_preset("high-margin", GOODINFO_URL, base_dir=tmp_path)

    assert preset.source == "goodinfo"
    assert preset.url == GOODINFO_URL

    presets = load_presets(tmp_path)
    assert list(presets) == ["high-margin"]
    assert presets["high-margin"].url == GOODINFO_URL

    removed = remove_preset("high-margin", base_dir=tmp_path)
    assert removed.url == GOODINFO_URL
    assert load_presets(tmp_path) == {}


def test_add_preset_rejects_duplicate_without_force(tmp_path: Path) -> None:
    add_preset("high-margin", GOODINFO_URL, base_dir=tmp_path)

    with pytest.raises(PresetExistsError):
        add_preset("high-margin", GOODINFO_URL, base_dir=tmp_path)

    updated = add_preset("high-margin", GOODINFO_URL, force=True, base_dir=tmp_path)
    assert updated.url == GOODINFO_URL


def test_remove_missing_preset_raises(tmp_path: Path) -> None:
    init_store(tmp_path)

    with pytest.raises(PresetNotFoundError):
        remove_preset("missing", base_dir=tmp_path)


@pytest.mark.parametrize("name", ["high-margin", "abc_123", "A-1"])
def test_validate_preset_name_accepts_supported_names(name: str) -> None:
    validate_preset_name(name)


@pytest.mark.parametrize("name", ["", "-bad", "bad name", "中文", "x" * 65])
def test_validate_preset_name_rejects_unsupported_names(name: str) -> None:
    with pytest.raises(InvalidPresetNameError):
        validate_preset_name(name)


@pytest.mark.parametrize(
    "url",
    [
        "http://goodinfo.tw/tw/StockList.asp",
        "https://example.com/tw/StockList.asp",
        "https://goodinfo.tw/tw/StockDetail.asp",
    ],
)
def test_validate_goodinfo_url_rejects_unsupported_urls(url: str) -> None:
    with pytest.raises(InvalidGoodinfoUrlError):
        validate_goodinfo_url(url)
