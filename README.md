# goodinfo-screener-cli

A command-line tool for saving and running Goodinfo stock screener presets with a local automated browser.

The goal is simple: turn a Goodinfo screener URL that you already use manually into a repeatable CLI workflow that can display results in the terminal and export them to CSV or JSON.

## Status

This project is preparing its first `v0.1.0` MVP release.

The first milestone is a minimal CLI that can:

- Save a Goodinfo stock screener URL as a named preset
- Open the preset URL with Playwright
- Wait for the screener result table to load
- Parse the visible table rows
- Print results as a terminal table
- Export results as CSV or JSON

## Installation

This project currently targets Python 3.11 or newer.

Install from a local checkout:

```bash
git clone https://github.com/pm7913/goodinfo-screener-cli.git
cd goodinfo-screener-cli
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Install Playwright's Chromium browser when working on browser automation:

```bash
playwright install chromium
```

Verify the CLI:

```bash
goodinfo --help
goodinfo --version
```

## Quick Start

Create the local preset store:

```bash
goodinfo init
```

Save a Goodinfo stock screener URL as a preset:

```bash
goodinfo import high-margin "https://goodinfo.tw/tw/StockList.asp?..."
```

Run the preset and print a readable preview:

```bash
goodinfo run high-margin --limit 10 --column-limit 8
```

Export the parsed rows:

```bash
goodinfo run high-margin \
  --csv results/high-margin.csv \
  --json results/high-margin.json
```

Debug Goodinfo page changes with a visible browser and rendered HTML output:

```bash
goodinfo run high-margin --headful --html fixtures/high-margin.html
```

See [examples/high-margin.yml](examples/high-margin.yml) for a sample preset based on a cumulative net profit margin screener.

## Development

This repository uses a pull request workflow for changes after the initial scaffold.

Recommended flow:

```bash
git switch main
git pull
git switch -c feat/<short-change-name>
```

Run tests:

```bash
pytest
```

Run lint checks:

```bash
ruff check .
```

Day 1 development status:

- Python package scaffold exists
- `goodinfo` CLI entrypoint exists
- Planned commands are visible in `goodinfo --help`
- Placeholder commands exit with clear milestone messages
- Basic CLI tests are included

Day 2 development status:
- `goodinfo init` creates the local preset YAML store
- `goodinfo import <name> <url>` saves a Goodinfo `StockList.asp` URL
- `goodinfo list` prints saved presets
- `goodinfo remove <name>` deletes a preset
- Preset names and Goodinfo URLs are validated
- Duplicate presets require `--force`
- Preset storage tests run without network access
See [CONTRIBUTING.md](CONTRIBUTING.md) for the PR workflow, local checks, and responsible-use contribution guidelines.

Day 3 development status:

- `goodinfo run <name>` loads a saved preset and opens it with Playwright
- `--headful` runs Chromium in visible mode for debugging
- `--timeout` controls browser timeout in milliseconds
- The browser runner waits for a supported Goodinfo stock result table
- `--html <path>` can save rendered HTML for debugging or future parser fixtures
- CSV and JSON export remain blocked until Day 4/5 table parsing is implemented

Day 4 development status:

- `parser.py` locates the rendered Goodinfo stock result table
- Table parsing extracts normalized headers and stock data rows
- Duplicate or blank headers are made stable for dictionary output
- Non-stock rows are skipped using Taiwan stock code detection
- `goodinfo run <name>` now reports the parsed row count after browser loading
- Parser tests use synthetic fixtures and do not commit Goodinfo HTML snapshots

Day 5 development status:

- `goodinfo run <name>` prints parsed rows as a terminal table
- `--limit <n>` controls how many rows are printed; `--limit 0` prints all rows
- `--column-limit <n>` controls how many columns are printed; `--column-limit 0` prints all columns
- `--csv <path>` writes parsed rows as UTF-8 BOM CSV for spreadsheet compatibility
- `--json <path>` writes parsed rows as pretty UTF-8 JSON
- CSV and JSON exporters preserve first-seen column order across parsed rows
- Exporter tests cover terminal output, CSV, JSON, and empty result handling

Day 6 development status:

- README includes quick start and troubleshooting notes
- `examples/high-margin.yml` provides a sample preset file
- GitHub Actions CI runs `pytest` and `ruff check .`
- Bug report and feature request issue templates are included

Day 7 development status:

- `CHANGELOG.md` documents the initial `v0.1.0` MVP
- Package version is set to `0.1.0`
- Version consistency is covered by tests
- GitHub release should be created after the stacked milestone PRs are merged into `main`

## Release Checklist

Before creating `v0.1.0` on GitHub:

- [ ] Merge Day 2 preset system PR
- [ ] Merge Day 3 browser runner PR
- [ ] Merge Day 4 parser PR
- [ ] Merge Day 5 output/export PR
- [ ] Merge Day 6 docs/CI PR
- [ ] Merge Day 7 release prep PR
- [ ] Confirm GitHub Actions CI passes on `main`
- [ ] Run one local Goodinfo smoke test
- [ ] Create GitHub release `v0.1.0`

## Future Roadmap Issues

- [Support CLI-defined screener filters](https://github.com/pm7913/goodinfo-screener-cli/issues/7)
- [Improve parser resilience for Goodinfo layout changes](https://github.com/pm7913/goodinfo-screener-cli/issues/8)
- [Add optional local caching for recent runs](https://github.com/pm7913/goodinfo-screener-cli/issues/9)
- [Package and release distribution workflow](https://github.com/pm7913/goodinfo-screener-cli/issues/10)

## Troubleshooting

### Playwright Browser Is Not Installed

If `goodinfo run` fails because Chromium is missing, install it:

```bash
playwright install chromium
```

### Goodinfo Page Loads But Parsing Fails

Goodinfo may change table markup over time. Re-run with rendered HTML output:

```bash
goodinfo run high-margin --html fixtures/high-margin.html
```

Then inspect whether the stock result table still uses `#tblStockList` or a recognizable stock table structure.

### Terminal Table Is Too Wide

Goodinfo tables can have many columns. Limit the preview:

```bash
goodinfo run high-margin --limit 10 --column-limit 8
```

Use `--column-limit 0` only when your terminal is wide enough.

### Browser Launch Fails On macOS

Headless browser launch can fail in restricted sandbox environments. Try running from a normal terminal session, or use:

```bash
goodinfo run high-margin --headful
```

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

## One-Week Milestone Plan

The goal for the first week is to ship `v0.1.0`: a usable MVP that can save a Goodinfo screener URL, run it through a local automated browser, parse the rendered result table, and export the result.

### Day 1: Project Scaffold and Development Environment

Milestone:

- Create the Python package structure
- Add `pyproject.toml`
- Add dependencies: `typer`, `rich`, `playwright`, `beautifulsoup4`, `pydantic`, and `pytest`
- Create the CLI entrypoint
- Add `ruff` for linting

Checkpoint:

```bash
goodinfo --help
pytest
ruff check .
```

Done when:

- The package can be installed locally
- `goodinfo --help` works
- README includes installation and development instructions

### Day 2: Preset System

Milestone:

- Implement `goodinfo init`
- Implement `goodinfo import <name> <url>`
- Implement `goodinfo list`
- Implement `goodinfo remove`
- Store presets in `~/.config/goodinfo-screener-cli/presets.yml`
- Validate preset names and Goodinfo URLs

Checkpoint:

```bash
goodinfo init
goodinfo import high-margin "https://goodinfo.tw/tw/StockList.asp?..."
goodinfo list
goodinfo remove high-margin
pytest tests/test_presets.py
```

Done when:

- Presets can be added, listed, and removed
- Duplicate preset names fail clearly
- Non-Goodinfo URLs fail clearly
- Preset tests run without network access

### Day 3: Browser Runner

Milestone:

- Implement a Playwright browser runner
- Support `--headful`
- Support `--timeout`
- Open the saved preset URL
- Wait for the Goodinfo page to load
- Return rendered HTML for parsing
- Provide clear timeout and table-missing errors

Checkpoint:

```bash
playwright install chromium
goodinfo run high-margin --headful
goodinfo run high-margin --timeout 45000
```

Done when:

- The browser can open a Goodinfo screener URL
- Headless and headful modes both work
- Failures produce readable error messages

### Day 4: Table Parser

Milestone:

- Implement `parser.py`
- Locate the main stock list result table
- Extract headers
- Extract rows
- Normalize whitespace
- Return `list[dict[str, str]]`
- Add saved HTML fixture tests

Checkpoint:

```bash
pytest tests/test_parser.py
```

Done when:

- Parser tests do not require network access
- A saved Goodinfo HTML fixture can be parsed
- Original Goodinfo column names are preserved where possible

### Day 5: Output and Export

Milestone:

- Print terminal tables with `rich`
- Implement CSV export
- Implement JSON export
- Use UTF-8 BOM for CSV spreadsheet compatibility
- Handle empty result sets clearly

Checkpoint:

```bash
goodinfo run high-margin
goodinfo run high-margin --csv results/high-margin.csv
goodinfo run high-margin --json results/high-margin.json
pytest tests/test_exporters.py
```

Done when:

- Terminal output is readable
- CSV and JSON export work
- Exported rows match the parsed terminal output

### Day 6: Integration, Docs, and CI

Milestone:

- Add installation instructions
- Add quick start instructions
- Add `examples/high-margin.yml`
- Add troubleshooting notes
- Add GitHub issue templates
- Add GitHub Actions CI for `pytest` and `ruff`

Checkpoint:

```bash
pytest
ruff check .
git status
```

Done when:

- A new user can follow the README and run the MVP
- CI runs automatically on GitHub
- At least one complete example workflow exists

### Day 7: v0.1.0 Release

Milestone:

- Run the full workflow end to end
- Polish README wording
- Add `CHANGELOG.md`
- Create GitHub release `v0.1.0`
- Add future roadmap issues

Checkpoint:

```bash
goodinfo import high-margin "<real-goodinfo-url>"
goodinfo run high-margin --headful
goodinfo run high-margin --csv results/high-margin.csv
pytest
ruff check .
```

Done when:

- The GitHub repository has a `v0.1.0` release
- The README is complete enough for a new user
- The package can be cloned, installed, and run locally
- The project has clear future roadmap issues

### Scope Control for Week One

Do not include these in the first-week MVP:

- Building every Goodinfo filter condition from CLI flags
- Scheduled jobs
- Bulk crawling
- Individual stock detail page crawling
- Login workflows
- Cookie management beyond normal browser behavior
- CAPTCHA handling
- Investment strategy recommendations

The first-week success criterion is intentionally narrow:

```text
Save a Goodinfo screener URL, run it from the CLI with Playwright, parse the rendered table, and export the result.
```

## Non-Goals

- No CAPTCHA bypassing
- No hidden API reverse engineering as the default approach
- No bulk historical database mirroring
- No investment advice or trading recommendations

## Disclaimer

This project is for research and workflow automation only. It does not provide investment advice. Stock market data may be delayed, incomplete, or incorrect. Always verify data before making financial decisions.

## License

MIT
