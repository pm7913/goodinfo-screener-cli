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


def test_placeholder_command_exits_with_clear_message() -> None:
    result = runner.invoke(app, ["init"])

    assert result.exit_code == 2
    assert "Day 2: Preset System" in result.output
