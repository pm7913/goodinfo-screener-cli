from typer.testing import CliRunner

from goodinfo_screener import __version__
from goodinfo_screener.browser import BrowserRunResult
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


def test_run_uses_browser_runner_for_saved_preset(tmp_path, monkeypatch) -> None:
    env = {"GOODINFO_SCREENER_CONFIG_DIR": str(tmp_path)}
    goodinfo_url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=test"
    runner.invoke(app, ["import", "high-margin", goodinfo_url], env=env)

    calls = {}

    def fake_run_goodinfo_page(url: str, *, headless: bool, timeout_ms: int) -> BrowserRunResult:
        calls["url"] = url
        calls["headless"] = headless
        calls["timeout_ms"] = timeout_ms
        return BrowserRunResult(
            final_url=url,
            title="Goodinfo Test",
            html="<html><table id='tblStockList'></table></html>",
            table_selector="#tblStockList",
        )

    monkeypatch.setattr("goodinfo_screener.cli.run_goodinfo_page", fake_run_goodinfo_page)

    result = runner.invoke(
        app,
        ["run", "high-margin", "--headful", "--timeout", "45000"],
        env=env,
    )

    assert result.exit_code == 0
    assert calls == {
        "url": goodinfo_url,
        "headless": False,
        "timeout_ms": 45000,
    }
    assert "Goodinfo Test" in result.output
    assert "#tblStockList" in result.output


def test_run_can_write_rendered_html(tmp_path, monkeypatch) -> None:
    env = {"GOODINFO_SCREENER_CONFIG_DIR": str(tmp_path / "config")}
    output = tmp_path / "rendered" / "goodinfo.html"
    goodinfo_url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=test"
    runner.invoke(app, ["import", "high-margin", goodinfo_url], env=env)

    def fake_run_goodinfo_page(url: str, *, headless: bool, timeout_ms: int) -> BrowserRunResult:
        return BrowserRunResult(
            final_url=url,
            title="Goodinfo Test",
            html="<html><table id='tblStockList'></table></html>",
            table_selector="#tblStockList",
        )

    monkeypatch.setattr("goodinfo_screener.cli.run_goodinfo_page", fake_run_goodinfo_page)

    result = runner.invoke(app, ["run", "high-margin", "--html", str(output)], env=env)

    assert result.exit_code == 0
    assert output.read_text(encoding="utf-8") == "<html><table id='tblStockList'></table></html>"
    assert "Rendered HTML written to" in result.output


def test_run_requires_existing_preset(tmp_path) -> None:
    env = {"GOODINFO_SCREENER_CONFIG_DIR": str(tmp_path)}

    result = runner.invoke(app, ["run", "missing"], env=env)

    assert result.exit_code == 1
    assert "Preset `missing` does not exist" in result.stderr


def test_run_rejects_exports_until_parser_exists(tmp_path) -> None:
    env = {"GOODINFO_SCREENER_CONFIG_DIR": str(tmp_path)}
    goodinfo_url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=test"
    runner.invoke(app, ["import", "high-margin", goodinfo_url], env=env)

    result = runner.invoke(app, ["run", "high-margin", "--csv", "out.csv"], env=env)

    assert result.exit_code == 1
    assert "CSV and JSON export are planned for Day 5" in result.stderr
