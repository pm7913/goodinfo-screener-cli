# Changelog

## v0.1.1 - 2026-06-02

Documentation and distribution metadata update.

### Added

- PyPI Trusted Publishing workflow for GitHub Actions
- PyPI version and download badges in README
- Project health page with impact signals, maintenance activity, roadmap
  evidence, package distribution status, and AI-assisted maintenance plan
- AI-assisted maintenance guidance in contributing docs and pull request
  template

### Verification

- `pytest`
- `ruff check .`
- `python -m build`
- GitHub Actions `Publish to PyPI` workflow successfully published `v0.1.0`
  through PyPI Trusted Publishing

## v0.1.0 - 2026-06-01

Initial MVP release.

### Added

- Python package scaffold with `goodinfo` CLI entrypoint
- Local YAML preset storage
- `goodinfo init`
- `goodinfo import <name> <url>`
- `goodinfo list`
- `goodinfo remove <name>`
- Goodinfo `StockList.asp` URL validation
- Playwright browser runner for saved screener URLs
- `goodinfo run <name>`
- `--headful` browser debug mode
- `--timeout` browser timeout option
- `--html` rendered HTML debug output
- Goodinfo stock result table parser
- Parsed row count in browser run output
- Rich terminal table output
- `--limit` terminal row preview limit
- `--column-limit` terminal column preview limit
- UTF-8 BOM CSV export with `--csv`
- Pretty UTF-8 JSON export with `--json`
- Example preset in `examples/high-margin.yml`
- GitHub Actions CI for tests and linting
- Bug report and feature request issue templates

### Responsible Use

- No CAPTCHA bypassing
- No bulk crawling
- No login-only automation
- No investment advice or trading recommendations
- Parser tests use synthetic fixtures instead of redistributing Goodinfo HTML snapshots

### Verification

- `pytest`
- `ruff check .`
- Manual Goodinfo smoke test parsed 206 rows from a saved screener URL
- CSV smoke output contained 207 lines: one header row plus 206 data rows
- JSON smoke output contained 206 data rows
