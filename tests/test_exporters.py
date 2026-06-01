import json
from pathlib import Path

import pytest
from rich.console import Console

from goodinfo_screener.exporters import (
    ExportError,
    ordered_fieldnames,
    render_rows_table,
    write_csv,
    write_json,
)

ROWS = [
    {"股票代號": "2330", "股票名稱": "台積電", "累季-淨利率(%)": "42.1"},
    {"股票代號": "2454", "股票名稱": "聯發科", "市場": "上市"},
]


def test_ordered_fieldnames_uses_first_seen_order() -> None:
    assert ordered_fieldnames(ROWS) == ["股票代號", "股票名稱", "累季-淨利率(%)", "市場"]


def test_write_csv_uses_utf8_sig_and_union_headers(tmp_path: Path) -> None:
    output = tmp_path / "results" / "rows.csv"

    write_csv(ROWS, output)

    data = output.read_bytes()
    assert data.startswith(b"\xef\xbb\xbf")
    text = output.read_text(encoding="utf-8-sig")
    assert "股票代號,股票名稱,累季-淨利率(%),市場" in text
    assert "2330,台積電,42.1," in text
    assert "2454,聯發科,,上市" in text


def test_write_json_uses_utf8_pretty_output(tmp_path: Path) -> None:
    output = tmp_path / "results" / "rows.json"

    write_json(ROWS, output)

    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded == ROWS
    assert "\n  {" in output.read_text(encoding="utf-8")


def test_exporters_reject_empty_rows(tmp_path: Path) -> None:
    with pytest.raises(ExportError):
        write_csv([], tmp_path / "empty.csv")

    with pytest.raises(ExportError):
        write_json([], tmp_path / "empty.json")


def test_render_rows_table_outputs_rows() -> None:
    console = Console(record=True, width=100)

    render_rows_table(ROWS, console=console, title="Rows", limit=1)

    output = console.export_text()
    assert "Rows" in output
    assert "2330" in output
    assert "台積電" in output
    assert "Showing 1 of 2 rows" in output


def test_render_rows_table_can_limit_columns() -> None:
    console = Console(record=True, width=100)

    render_rows_table(ROWS, console=console, title="Rows", limit=1, column_limit=2)

    output = console.export_text()
    assert "股票代號" in output
    assert "股票名稱" in output
    assert "累季-淨利率" not in output
    assert "Showing 2 of 3 columns" in output
