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

## MVP Specification

The first implementation focuses on Goodinfo stock screener result pages that are already represented by a full URL.

### In Scope

- Import a Goodinfo `StockList.asp` screener URL as a named preset
- Store presets in a local config directory
- Run one preset at a time
- Launch Chromium with Playwright
- Load the saved Goodinfo screener URL
- Wait until the stock list table is visible and no longer showing a loading state
- Extract table headers and rows from the rendered page
- Print results in the terminal
- Export the same parsed rows to CSV or JSON

### Out of Scope for MVP

- Building every Goodinfo filter condition from CLI flags
- Running many presets in parallel
- Crawling individual stock detail pages
- Running scheduled jobs
- Login-only workflows
- CAPTCHA handling or bypassing

## Command Behavior

### `goodinfo init`

Creates the local config directory and an empty preset file if they do not already exist.

Expected default location:

```text
~/.config/goodinfo-screener-cli/
  presets.yml
```

### `goodinfo import <preset-name> <goodinfo-url>`

Validates and stores a preset.

Rules:

- `<preset-name>` must be unique
- URL must use `https://goodinfo.tw/`
- URL path should target `/tw/StockList.asp`
- Existing presets are not overwritten unless `--force` is passed

Example:

```bash
goodinfo import high-margin "https://goodinfo.tw/tw/StockList.asp?..."
```

### `goodinfo list`

Prints saved presets with their name, source, created time, and URL.

### `goodinfo run <preset-name>`

Loads a saved preset, opens the URL in Playwright, parses the rendered table, and prints rows in a terminal table.

Useful options:

```bash
goodinfo run high-margin --headful
goodinfo run high-margin --timeout 45000
goodinfo run high-margin --csv results/high-margin.csv
goodinfo run high-margin --json results/high-margin.json
```

### `goodinfo remove <preset-name>`

Deletes a saved preset from the local preset file.

## Proposed Configuration

Presets may be stored locally as YAML:

```yaml
presets:
  high-margin:
    source: goodinfo
    url: "https://goodinfo.tw/tw/StockList.asp?..."
    created_at: "2026-05-31T00:00:00Z"
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

## Implementation Design

### CLI Layer

`cli.py` owns command parsing and user-facing errors. It should stay thin and delegate work to smaller modules.

Responsibilities:

- Parse command arguments with `typer`
- Load user config
- Call preset, browser, parser, and exporter services
- Return non-zero exit codes for invalid presets, failed page loads, and export errors

### Preset Storage

`presets.py` manages local YAML storage.

Responsibilities:

- Create the config directory
- Read and write `presets.yml`
- Validate preset names and Goodinfo URLs
- Prevent accidental overwrite unless `--force` is used

### Browser Runner

`browser.py` wraps Playwright.

Expected flow:

1. Start Chromium in headless mode by default
2. Open the preset URL
3. Accept or dismiss the cookie notice when visible
4. Wait for the loading text to disappear
5. Wait for a stock result table to become visible
6. Return the final page HTML to the parser
7. Close the browser context

The runner should expose a `--headful` mode so users can inspect Goodinfo behavior when selectors change.

### Table Parser

`parser.py` converts the rendered HTML into normalized rows.

Initial strategy:

- Locate the main stock list result table
- Extract visible header cells
- Extract visible body rows
- Normalize whitespace
- Preserve original column names from Goodinfo
- Return `list[dict[str, str]]`

The parser should not make investment-specific assumptions in the MVP. It should preserve the table as shown rather than attempting to rename every financial metric.

### Exporters

`exporters.py` writes parsed rows to disk.

Supported MVP formats:

- CSV with UTF-8 BOM for spreadsheet compatibility
- JSON with UTF-8 encoding and pretty indentation

### Error Handling

The CLI should produce clear errors for:

- Missing preset
- Invalid Goodinfo URL
- Browser timeout
- Result table not found
- Empty result set
- Export path not writable

### Testing Strategy

Early tests should avoid hitting Goodinfo directly.

Recommended tests:

- Preset name validation
- URL validation
- YAML read/write round trip
- Parser tests using saved HTML fixtures
- CSV and JSON exporter tests

Live browser tests can be added later and marked separately because they depend on network and Goodinfo page behavior.

## Acceptance Criteria for v0.1.0

Version `0.1.0` is considered complete when a user can:

1. Install the package locally
2. Import a Goodinfo screener URL as a preset
3. List saved presets
4. Run the preset through Playwright
5. See parsed rows in the terminal
6. Export the same result to CSV
7. Run parser and preset tests locally without network access

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
