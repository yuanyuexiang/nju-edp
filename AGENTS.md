# Repository Guidelines

## Project Structure & Module Organization

This repository is a Chinese-language Nanjing University EDP admissions marketing research package. Research documents live in the root; video deliverables and their rendering scripts live under `assets/video/`.

- `README.md` indexes the deliverables and explains the recommended execution sequence.
- `01-*.md`, `02-*.md`, `06-*.md`, and `08-*.md` cover strategy, the 90-day plan, interviews, and platform operations.
- `07-来源清单.md` records research sources and limitations.
- `03-*.csv` and `09-*.csv` contain publishing calendars; `04-*.csv` is the CRM template; `05-*.csv` is the metrics dashboard.

## Development & Validation Commands

No application build or automated tests are configured. Edit Markdown and CSV directly; follow each video directory’s README to regenerate media.

- `git status --short`: inspect pending changes before and after editing.
- `git diff --check`: detect whitespace errors before committing.
- `git diff -- '*.md' '*.csv'`: review content and template changes.
- `rg '^#{1,3} ' -- *.md`: inspect document heading structure.

## Content Style & Naming Conventions

Write research and operational content in simplified Chinese. Follow the existing `NN-中文标题.md` or `NN-中文标题.csv` naming pattern for new deliverables, and add them to `README.md`.

Use one top-level Markdown title, descriptive subheadings, short paragraphs, and actionable lists. Match each document’s existing numbering and table style. No formatter, linter, or fixed indentation standard is configured; use spaces and preserve surrounding formatting.

Keep CSV headers and column order stable. Quote fields containing commas, including dashboard formulas, and preserve UTF-8 Chinese text. Recheck formula references whenever columns move.

## Testing Guidelines

There is no test framework or coverage target. Preview changed Markdown and check links, tables, dates, and cross-document consistency. Parse changed CSVs with a CSV-aware reader and confirm every nonblank row matches the header’s column count. Open affected templates in a spreadsheet tool to verify Chinese text and formulas. Keep sample rows clearly labeled.

## Commit & Pull Request Guidelines

History contains only `first commit`, so no established commit convention exists. Use concise, descriptive subjects such as `docs: update 30-day publishing schedule`. Keep commits focused.

PRs should explain the purpose, affected deliverables, supporting sources, and validation performed. Link related issues when available; include screenshots only when presentation changes need visual review.

## Research & Data Handling

Record new research sources in `07-来源清单.md`. Distinguish verified facts from assumptions. Follow the README’s requirement that unverified fees, dates, faculty, certificates, and benefits use the center’s final approved wording. Keep personal lead data out of committed CRM templates, and exclude local artifacts such as `.DS_Store`.
