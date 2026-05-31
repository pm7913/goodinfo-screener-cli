# goodinfo-screener-cli

A command-line tool for saving and running Goodinfo stock screener presets with a local automated browser.

The goal is simple: turn a Goodinfo screener URL that you already use manually into a repeatable CLI workflow that can display results in the terminal and export them to CSV or JSON.

## Status

This project is in early planning and scaffolding stage.

The first milestone is a minimal CLI that can:

- Save a Goodinfo stock screener URL as a named preset
- Open the preset URL with Playwright
- Wait for the screener result table to load
- Parse the visible table rows
- Print results as a terminal table
- Export results as CSV or JSON

## Why This Exists

Goodinfo provides a useful Taiwan stock screening interface, but repeated manual screening can become tedious:

- Opening the same saved filter URL
- Waiting for the table to load
- Copying rows into a spreadsheet
- Repeating the same workflow later

`goodinfo-screener-cli` is intended to automate that personal workflow while keeping the browser behavior transparent and user-controlled.

## Example Use Case

Given a Goodinfo custom screener URL such as a filter for:

- Market: listed and OTC stocks
- Sheet: quarterly cumulative profitability
- Metric: cumulative net profit margin
- Condition: greater than or equal to 30%

You could save it as a preset:

```bash
goodinfo import high-margin "https://goodinfo.tw/tw/StockList.asp?..."
```

Then run it later:

```bash
goodinfo run high-margin
```

Export results:

```bash
goodinfo run high-margin --csv results/high-margin.csv
goodinfo run high-margin --json results/high-margin.json
```

Run with a visible browser for debugging:

```bash
goodinfo run high-margin --headful
```

## Proposed CLI

```bash
goodinfo init
goodinfo import <preset-name> <goodinfo-url>
goodinfo list
goodinfo run <preset-name>
goodinfo run <preset-name> --csv output.csv
goodinfo run <preset-name> --json output.json
goodinfo remove <preset-name>
```

## Proposed Configuration

Presets may be stored locally as YAML:

```yaml
name: high-margin
source: goodinfo
url: "https://goodinfo.tw/tw/StockList.asp?..."
browser:
  headless: true
  timeout_ms: 30000
output:
  format: table
```

## Technical Plan

The initial implementation is planned in Python:

- `typer` for the CLI
- `rich` for terminal tables
- `playwright` for browser automation
- `beautifulsoup4` or `lxml` for table parsing
- `pydantic` for preset validation

Planned package layout:

```text
goodinfo_screener/
  cli.py
  browser.py
  parser.py
  presets.py
  exporters.py
tests/
examples/
```

## Responsible Use

This project is designed for low-frequency personal research automation, not bulk scraping.

Expected safeguards:

- Use a real local browser session
- Avoid high-frequency requests
- Add local caching where practical
- Do not bypass CAPTCHAs, paywalls, account restrictions, or access controls
- Do not redistribute proprietary datasets
- Respect Goodinfo's terms, privacy policy, and website availability

Users are responsible for ensuring their use complies with Goodinfo's terms and applicable laws.

## Roadmap

- [ ] Create Python package scaffold
- [ ] Add `goodinfo import`
- [ ] Add local preset storage
- [ ] Add Playwright browser runner
- [ ] Parse Goodinfo screener result tables
- [ ] Add terminal table output
- [ ] Add CSV and JSON exporters
- [ ] Add tests for preset loading and table parsing
- [ ] Add examples for common Taiwan stock screening workflows

## Non-Goals

- No CAPTCHA bypassing
- No hidden API reverse engineering as the default approach
- No bulk historical database mirroring
- No investment advice or trading recommendations

## Disclaimer

This project is for research and workflow automation only. It does not provide investment advice. Stock market data may be delayed, incomplete, or incorrect. Always verify data before making financial decisions.

## License

MIT
