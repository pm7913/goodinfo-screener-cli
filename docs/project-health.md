# Project Health

This page collects review-friendly evidence about the public health,
maintenance cadence, and AI-assisted maintenance workflow for
`goodinfo-screener-cli`.

Last updated: 2026-06-02.

## Reviewer Summary

`goodinfo-screener-cli` is a new, actively maintained MIT-licensed Python CLI
for repeatable, local Goodinfo stock screener workflows. The first public
release shipped through a focused PR sequence with CI, tests, issue templates, a
documented roadmap, and responsible-use guardrails. Codex will be integrated
into daily maintenance for review, issue triage, test planning, changelog
drafting, documentation upkeep, and release-readiness checks.

## Impact Signals

`goodinfo-screener-cli` is an early public project focused on a narrow,
user-controlled workflow: saving Goodinfo stock screener presets, running them
locally with Playwright, and exporting parsed rows to CSV or JSON.

Current public signals:

- Repository: https://github.com/pm7913/goodinfo-screener-cli
- Visibility: public
- License: MIT
- Primary language: Python
- GitHub topics: `python`, `cli`, `goodinfo`, `stock-screener`,
  `taiwan-stocks`, `playwright`, `browser-automation`, `csv`, `json`, `rich`,
  `typer`
- GitHub topic discovery: listed under the public `stock-screener` topic for
  Python repositories
- Stars: 0
- Forks: 0
- Watchers: 0
- Contributors: 1 known maintainer in public git history
- Package manager distribution: PyPI release workflow prepared with GitHub
  Actions Trusted Publishing; PyPI pending publisher configured; first PyPI
  release pending
- Downstream dependents: none known yet

The project is intentionally transparent about being new. Near-term impact work
is tracked in the roadmap, with package distribution prepared before collecting
download or downstream-dependency metrics.

## Package Manager Distribution

The repository now includes `.github/workflows/publish.yml` for PyPI releases.
The workflow runs when a GitHub release is published, builds the package, and
publishes it through PyPI Trusted Publishing.

The PyPI pending trusted publisher is configured for:

- PyPI project name: `goodinfo-screener-cli`
- Provider: GitHub
- Repository: `pm7913/goodinfo-screener-cli`
- Workflow: `publish.yml`
- Environment: `pypi`

Expected installation command after the first successful PyPI release:

```bash
python -m pip install goodinfo-screener-cli
```

After the first successful PyPI release, this page should track:

- PyPI project URL
- PyPI version badge
- PyPI download badge or download query result
- Monthly download trend
- Known downstream dependents, if any

## Maintenance Activity

Recent activity as of 2026-06-02:

- Created: 2026-05-31
- Latest push: 2026-06-01
- Latest release: `v0.1.0`, published 2026-06-01
- Merged pull requests: 7
- Open roadmap issues: 4
- CI: GitHub Actions runs tests and linting on pushes to `main` and pull
  requests
- Release verification: `pytest`, `ruff check .`, CLI help smoke test, and a
  manual Goodinfo smoke test are documented in `CHANGELOG.md`

The initial release was built through focused pull requests:

- PR #1: pull request workflow docs
- PR #2: preset storage commands
- PR #3: Playwright browser runner
- PR #4: Goodinfo table parser
- PR #5: table output and CSV/JSON exporters
- PR #6: docs, examples, CI, and issue templates
- PR #11: `v0.1.0` release preparation

## Roadmap

The current roadmap is tracked in GitHub issues:

- Issue #7: support CLI-defined screener filters
- Issue #8: improve parser resilience for Goodinfo layout changes
- Issue #9: add optional local caching for recent runs
- Issue #10: package and release distribution workflow

The roadmap keeps the scope aligned with responsible personal research
automation. Bulk crawling, login-only automation, CAPTCHA bypassing, hidden API
reverse engineering by default, and investment recommendations are out of scope.

## AI-Assisted Maintenance Plan

Codex will be used as a maintenance assistant, not as an unsupervised release
authority. The maintainer remains responsible for reviewing, testing, and
merging changes.

Planned Codex workflows:

- Code review: inspect focused pull requests for parser regressions,
  responsible-use risks, missing tests, and CLI usability problems.
- Issue triage: classify bug reports and feature requests by reproducibility,
  affected module, responsible-use risk, and roadmap fit.
- Test generation: propose focused unit tests for parser fixtures, exporter
  edge cases, and CLI validation paths before implementation changes are
  merged.
- Changelog drafting: summarize merged PRs into release notes, including
  verification steps and known limitations.
- Documentation maintenance: keep README examples, troubleshooting notes,
  roadmap links, and this project-health page current after releases.
- Release readiness checks: compare `CHANGELOG.md`, GitHub release notes, test
  status, and open roadmap issues before publishing a release.

Codex outputs should be treated as review input. Any AI-assisted change must
still pass CI and follow the contribution and responsible-use requirements in
`CONTRIBUTING.md`.
