"""Parse rendered Goodinfo stock screener tables."""

from __future__ import annotations

import re
from collections.abc import Iterable

from bs4 import BeautifulSoup, Tag

STOCK_CODE_RE = re.compile(r"^\d{4}[A-Za-z]?$")
HEADER_HINTS = ("股票代號", "代號", "股票名稱", "名稱")


class TableParseError(Exception):
    """Base error for table parsing."""


class StockTableParseError(TableParseError):
    """Raised when a stock table cannot be parsed from HTML."""


def normalize_text(value: str) -> str:
    """Normalize repeated whitespace in cell text."""
    return " ".join(value.split())


def cell_text(cell: Tag) -> str:
    """Extract normalized text from a table cell."""
    return normalize_text(cell.get_text(" ", strip=True))


def find_stock_table(html: str) -> Tag:
    """Find the Goodinfo stock list table in rendered HTML."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", id="tblStockList")
    if isinstance(table, Tag):
        return table

    for candidate in soup.find_all("table"):
        text = normalize_text(candidate.get_text(" ", strip=True))
        if "股票代號" in text or ("代號" in text and "名稱" in text):
            return candidate

    raise StockTableParseError("Could not locate a Goodinfo stock result table in HTML.")


def row_cells(row: Tag) -> list[str]:
    """Return direct table cell text for one row."""
    cells = row.find_all(["th", "td"], recursive=False)
    return [cell_text(cell) for cell in cells]


def row_has_header_hints(cells: Iterable[str]) -> bool:
    """Return whether a row looks like a Goodinfo header row."""
    joined = " ".join(cells)
    return any(hint in joined for hint in HEADER_HINTS)


def row_has_stock_code(cells: list[str]) -> bool:
    """Return whether a row appears to contain a Taiwan stock code."""
    return any(STOCK_CODE_RE.fullmatch(cell) for cell in cells[:5])


def unique_headers(headers: list[str]) -> list[str]:
    """Ensure headers can be used as stable dictionary keys."""
    counts: dict[str, int] = {}
    unique: list[str] = []

    for index, header in enumerate(headers, start=1):
        base = header or f"Column {index}"
        counts[base] = counts.get(base, 0) + 1
        if counts[base] == 1:
            unique.append(base)
        else:
            unique.append(f"{base}_{counts[base]}")

    return unique


def find_header_index(rows: list[list[str]]) -> int:
    """Find the most likely header row index."""
    for index, cells in enumerate(rows):
        if row_has_header_hints(cells):
            return index
    if rows:
        return 0
    raise StockTableParseError("Stock table does not contain any rows.")


def normalize_row_to_headers(headers: list[str], cells: list[str]) -> dict[str, str]:
    """Map one table row to header keys, extending short header rows when needed."""
    if len(cells) > len(headers):
        extra_headers = [
            f"Column {index}"
            for index in range(len(headers) + 1, len(cells) + 1)
        ]
        headers = [*headers, *extra_headers]

    return {
        header: cells[index] if index < len(cells) else ""
        for index, header in enumerate(headers)
    }


def parse_stock_table(html: str) -> list[dict[str, str]]:
    """Parse a rendered Goodinfo stock result table into row dictionaries."""
    table = find_stock_table(html)
    rows = [cells for row in table.find_all("tr") if (cells := row_cells(row))]
    header_index = find_header_index(rows)
    headers = unique_headers(rows[header_index])

    parsed_rows: list[dict[str, str]] = []
    for cells in rows[header_index + 1 :]:
        if not row_has_stock_code(cells):
            continue
        parsed_rows.append(normalize_row_to_headers(headers, cells))

    if not parsed_rows:
        raise StockTableParseError("Stock table was found, but no stock data rows were parsed.")

    return parsed_rows
