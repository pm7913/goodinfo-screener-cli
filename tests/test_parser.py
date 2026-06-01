import pytest

from goodinfo_screener.parser import (
    StockTableParseError,
    normalize_text,
    parse_stock_table,
    unique_headers,
)


def test_normalize_text_collapses_repeated_whitespace() -> None:
    assert normalize_text("  股票\n  代號\t2330  ") == "股票 代號 2330"


def test_unique_headers_preserves_names_and_deduplicates() -> None:
    assert unique_headers(["股票代號", "名稱", "名稱", ""]) == [
        "股票代號",
        "名稱",
        "名稱_2",
        "Column 4",
    ]


def test_parse_stock_table_from_goodinfo_like_html() -> None:
    html = """
    <html>
      <body>
        <table id="tblStockList">
          <tr>
            <th>排名</th>
            <th>股票代號</th>
            <th>股票名稱</th>
            <th>市場</th>
            <th>累季-淨利率(%)</th>
          </tr>
          <tr>
            <td>1</td>
            <td>2330</td>
            <td>台積電</td>
            <td>上市</td>
            <td>42.1</td>
          </tr>
          <tr>
            <td>2</td>
            <td>2454</td>
            <td>聯發科</td>
            <td>上市</td>
            <td>31.8</td>
          </tr>
        </table>
      </body>
    </html>
    """

    rows = parse_stock_table(html)

    assert rows == [
        {
            "排名": "1",
            "股票代號": "2330",
            "股票名稱": "台積電",
            "市場": "上市",
            "累季-淨利率(%)": "42.1",
        },
        {
            "排名": "2",
            "股票代號": "2454",
            "股票名稱": "聯發科",
            "市場": "上市",
            "累季-淨利率(%)": "31.8",
        },
    ]


def test_parse_stock_table_skips_non_stock_rows() -> None:
    html = """
    <table id="tblStockList">
      <tr><th>股票代號</th><th>股票名稱</th></tr>
      <tr><td>小計</td><td>2</td></tr>
      <tr><td>2330</td><td>台積電</td></tr>
    </table>
    """

    rows = parse_stock_table(html)

    assert rows == [{"股票代號": "2330", "股票名稱": "台積電"}]


def test_parse_stock_table_falls_back_to_table_with_header_hints() -> None:
    html = """
    <table><tr><td>Not this table</td></tr></table>
    <table>
      <tr><td>代號</td><td>名稱</td></tr>
      <tr><td>2330</td><td>台積電</td></tr>
    </table>
    """

    rows = parse_stock_table(html)

    assert rows == [{"代號": "2330", "名稱": "台積電"}]


def test_parse_stock_table_raises_when_table_missing() -> None:
    with pytest.raises(StockTableParseError):
        parse_stock_table("<html><body>No table</body></html>")


def test_parse_stock_table_raises_when_no_data_rows() -> None:
    html = "<table id='tblStockList'><tr><th>股票代號</th><th>股票名稱</th></tr></table>"

    with pytest.raises(StockTableParseError, match="no stock data rows"):
        parse_stock_table(html)
