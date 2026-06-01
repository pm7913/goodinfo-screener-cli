"""Playwright browser runner for Goodinfo screener pages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

DEFAULT_TABLE_SELECTORS: Final[tuple[str, ...]] = (
    "#tblStockList",
    "table#tblStockList",
    "table:has-text('股票代號')",
    "table:has-text('股票名稱')",
)

COOKIE_DISMISS_SELECTORS: Final[tuple[str, ...]] = (
    "button:has-text('同意')",
    "button:has-text('接受')",
    "button:has-text('Accept')",
    "input[type='button'][value*='同意']",
    "input[type='button'][value*='接受']",
)


class BrowserError(Exception):
    """Base browser runner error."""


class BrowserTimeoutError(BrowserError):
    """Raised when the Goodinfo page does not load in time."""


class StockTableNotFoundError(BrowserError):
    """Raised when no supported stock table selector is found."""


@dataclass(frozen=True)
class BrowserRunResult:
    """Rendered Goodinfo page data returned by the browser runner."""

    final_url: str
    title: str
    html: str
    table_selector: str


def wait_for_stock_table(page, *, timeout_ms: int) -> str:
    """Wait for the first supported Goodinfo stock table selector."""
    for selector in DEFAULT_TABLE_SELECTORS:
        try:
            page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
            return selector
        except PlaywrightTimeoutError:
            continue

    joined = ", ".join(DEFAULT_TABLE_SELECTORS)
    raise StockTableNotFoundError(f"Could not find a Goodinfo stock result table. Tried: {joined}")


def dismiss_cookie_notice(page) -> None:
    """Best-effort dismissal for visible cookie notices."""
    for selector in COOKIE_DISMISS_SELECTORS:
        try:
            page.locator(selector).first.click(timeout=1000)
            return
        except PlaywrightTimeoutError:
            continue
        except Exception:
            continue


def run_goodinfo_page(
    url: str,
    *,
    headless: bool = True,
    timeout_ms: int = 30000,
) -> BrowserRunResult:
    """Open a Goodinfo screener URL and return rendered page HTML."""
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=headless)
            context = browser.new_context(
                locale="zh-TW",
                timezone_id="Asia/Taipei",
                viewport={"width": 1440, "height": 1000},
            )
            page = context.new_page()
            page.set_default_timeout(timeout_ms)

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
                dismiss_cookie_notice(page)
                selector = wait_for_stock_table(page, timeout_ms=timeout_ms)
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
                return BrowserRunResult(
                    final_url=page.url,
                    title=page.title(),
                    html=page.content(),
                    table_selector=selector,
                )
            finally:
                context.close()
                browser.close()
    except PlaywrightTimeoutError as exc:
        raise BrowserTimeoutError(f"Timed out while loading Goodinfo page: {url}") from exc
    except PlaywrightError as exc:
        raise BrowserError(f"Playwright browser run failed: {exc}") from exc


def write_rendered_html(result: BrowserRunResult, path: Path) -> Path:
    """Write rendered HTML to disk for debugging or parser fixture creation."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(result.html, encoding="utf-8")
    return path
