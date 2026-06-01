from typer.testing import CliRunner

from goodinfo_screener import __version__
from goodinfo_screener.cli import app

runner = CliRunner()


def test_help_shows_project_purpose() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Goodinfo stock screener presets" in result.output
    assert "init" in result.output
    assert "run" in result.output


def test_version_option() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_preset_workflow(tmp_path) -> None:
    env = {"GOODINFO_SCREENER_CONFIG_DIR": str(tmp_path)}
    goodinfo_url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=test"

    result = runner.invoke(app, ["init"], env=env)
    assert result.exit_code == 0
    assert "Preset store ready" in result.output

    result = runner.invoke(app, ["import", "high-margin", goodinfo_url], env=env)
    assert result.exit_code == 0
    assert "Saved preset `high-margin`" in result.output

    result = runner.invoke(app, ["list"], env=env)
    assert result.exit_code == 0
    assert "high-margin" in result.output
    assert "goodinfo" in result.output

    result = runner.invoke(app, ["remove", "high-margin"], env=env)
    assert result.exit_code == 0
    assert "Removed preset `high-margin`" in result.output

    result = runner.invoke(app, ["list"], env=env)
    assert result.exit_code == 0
    assert "No presets found" in result.output


def test_import_rejects_duplicate_without_force(tmp_path) -> None:
    env = {"GOODINFO_SCREENER_CONFIG_DIR": str(tmp_path)}
    goodinfo_url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=test"

    first = runner.invoke(app, ["import", "high-margin", goodinfo_url], env=env)
    assert first.exit_code == 0

    duplicate = runner.invoke(app, ["import", "high-margin", goodinfo_url], env=env)
    assert duplicate.exit_code == 1
    assert "already exists" in duplicate.stderr

    forced = runner.invoke(app, ["import", "high-margin", goodinfo_url, "--force"], env=env)
    assert forced.exit_code == 0
    assert "Updated preset `high-margin`" in forced.output


def test_import_rejects_invalid_name_and_url(tmp_path) -> None:
    env = {"GOODINFO_SCREENER_CONFIG_DIR": str(tmp_path)}

    invalid_name = runner.invoke(
        app,
        ["import", "bad name", "https://goodinfo.tw/tw/StockList.asp"],
        env=env,
    )
    assert invalid_name.exit_code == 1
    assert "Preset names must start" in invalid_name.stderr

    invalid_url = runner.invoke(
        app,
        ["import", "high-margin", "https://example.com/tw/StockList.asp"],
        env=env,
    )
    assert invalid_url.exit_code == 1
    assert "URL host must be goodinfo.tw" in invalid_url.stderr


def test_run_placeholder_remains_for_day_3() -> None:
    result = runner.invoke(app, ["run", "high-margin"])

    assert result.exit_code == 2
    assert "Day 3: Browser Runner" in result.output
