from pathlib import Path

import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from goodinfo_screener.browser import (
    BrowserError,
    BrowserRunResult,
    StockTableNotFoundError,
    run_goodinfo_page,
    wait_for_stock_table,
    write_rendered_html,
)


class FakePage:
    def __init__(self, visible_selector: str | None) -> None:
        self.visible_selector = visible_selector
        self.tried: list[str] = []

    def wait_for_selector(self, selector: str, *, state: str, timeout: int) -> None:
        self.tried.append(selector)
        assert state == "visible"
        assert timeout == 30000
        if selector != self.visible_selector:
            raise PlaywrightTimeoutError("not found")


def test_wait_for_stock_table_returns_first_visible_supported_selector() -> None:
    page = FakePage("table#tblStockList")

    selector = wait_for_stock_table(page, timeout_ms=30000)

    assert selector == "table#tblStockList"
    assert page.tried == ["#tblStockList", "table#tblStockList"]


def test_wait_for_stock_table_raises_when_no_selector_matches() -> None:
    page = FakePage(None)

    with pytest.raises(StockTableNotFoundError):
        wait_for_stock_table(page, timeout_ms=30000)


def test_write_rendered_html_creates_parent_directories(tmp_path: Path) -> None:
    result = BrowserRunResult(
        final_url="https://goodinfo.tw/tw/StockList.asp",
        title="Goodinfo Test",
        html="<html></html>",
        table_selector="#tblStockList",
    )
    output = tmp_path / "fixtures" / "goodinfo.html"

    written = write_rendered_html(result, output)

    assert written == output
    assert output.read_text(encoding="utf-8") == "<html></html>"


def test_run_goodinfo_page_wraps_playwright_launch_errors(monkeypatch) -> None:
    class BrokenChromium:
        def launch(self, *, headless: bool):
            raise PlaywrightError("launch failed")

    class FakePlaywright:
        chromium = BrokenChromium()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return None

    monkeypatch.setattr("goodinfo_screener.browser.sync_playwright", FakePlaywright)

    with pytest.raises(BrowserError, match="Playwright browser run failed"):
        run_goodinfo_page("https://goodinfo.tw/tw/StockList.asp", timeout_ms=1000)
