# Contributing

Thanks for your interest in improving `goodinfo-screener-cli`.

This project uses a lightweight pull request workflow so changes are reviewable and easy to trace.

## Development Workflow

1. Open or pick a GitHub issue for the work.
2. Create a branch from `main`.
3. Make a focused change.
4. Run local checks.
5. Open a pull request.
6. Merge after review and passing checks.

Branch naming examples:

```text
feat/preset-storage
feat/browser-runner
fix/url-validation
docs/quick-start
chore/ci
```

## Local Setup

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

## Required Checks

Run these before opening a pull request:

```bash
pytest
ruff check .
goodinfo --help
```

## Scope Guidelines

Keep PRs small and tied to one milestone when possible.

Good PR scopes:

- Add local preset storage
- Add Goodinfo URL validation
- Add CSV exporter
- Add parser fixtures
- Add README quick start

Avoid mixing unrelated work such as parser changes, browser automation, and release docs in a single PR unless they are tightly connected.

## Responsible Use Requirements

This project is intended for low-frequency personal research automation.

Contributions should not add:

- CAPTCHA bypassing
- High-frequency scraping behavior
- Bulk historical data mirroring
- Login-only workflow automation
- Hidden API reverse engineering as the default approach
- Investment advice or trading recommendations

If a change touches browser automation, include a note in the PR about how it respects the project's responsible-use policy.
