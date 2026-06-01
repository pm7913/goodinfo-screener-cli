"""Terminal and file exporters for parsed Goodinfo rows."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table


class ExportError(Exception):
    """Raised when parsed rows cannot be exported."""


def ordered_fieldnames(rows: list[dict[str, str]]) -> list[str]:
    """Return field names in first-seen order across all rows."""
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fields.append(key)
    return fields


def write_csv(rows: list[dict[str, str]], path: Path) -> Path:
    """Write rows as UTF-8 BOM CSV for spreadsheet compatibility."""
    if not rows:
        raise ExportError("Cannot export an empty result set to CSV.")

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ordered_fieldnames(rows)
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return path


def write_json(rows: list[dict[str, str]], path: Path) -> Path:
    """Write rows as pretty UTF-8 JSON."""
    if not rows:
        raise ExportError("Cannot export an empty result set to JSON.")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def render_rows_table(
    rows: list[dict[str, str]],
    *,
    console: Console,
    title: str,
    limit: int = 25,
    column_limit: int = 8,
) -> None:
    """Render parsed rows in a terminal table."""
    if not rows:
        raise ExportError("Cannot render an empty result set.")

    display_rows = rows if limit <= 0 else rows[:limit]
    all_fieldnames = ordered_fieldnames(display_rows)
    fieldnames = all_fieldnames if column_limit <= 0 else all_fieldnames[:column_limit]
    table = Table(title=title, show_lines=False)
    for field in fieldnames:
        table.add_column(field, overflow="fold")

    for row in display_rows:
        table.add_row(*(row.get(field, "") for field in fieldnames))

    console.print(table)
    if 0 < limit < len(rows):
        console.print(f"Showing {limit} of {len(rows)} rows. Use --limit 0 to show all rows.")
    if 0 < column_limit < len(all_fieldnames):
        console.print(
            f"Showing {column_limit} of {len(all_fieldnames)} columns. "
            "Use --column-limit 0 to show all columns."
        )
