---
aliases: [CHANGELOG]
tags: ['00_KnowledgeFramework', 'CHANGELOG']
---

# Changelog

All notable changes to TianshangKnowledgeBase will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- CI: Full wiki-link coverage check (3 types: simple-name, vault-root, relative path)
- CI: Frontmatter validation (aliases + tags required in every .md file)
- CI: File naming convention check (UpperCamelCase for English filenames)
- CI: Orphan file warning (files with no incoming wiki-links)
- Engineering: Shared `path_utils.py` module with auto BASE discovery
- Engineering: `requirements.txt` + `pyproject.toml` for dependency management
- Engineering: `CHANGELOG.md` for tracking changes
- Engineering: Pull request template (`.github/PULL_REQUEST_TEMPLATE.md`)
- Engineering: Pre-commit hook configuration (`.pre-commit-config.yaml`)

### Changed
- Refactored: 18 fix scripts now use `path_utils.BASE` instead of hardcoded paths
- Refined: `.gitignore` now tracks `.opencode/fixes/*.py` while ignoring root `.py` files

## [1.0.0] - 2026-05-18

### Added
- Initial knowledge base: 14 top-level discipline directories
- 2,301 Markdown files across 526 directories
- 100% INDEX.md coverage in every directory
- 100% YAML frontmatter (aliases + tags)
- UpperCamelCase naming convention for sub-directories and English filenames
- GitHub Actions CI with basic checks (U+FFFD, trailing whitespace, simple link check, INDEX completeness, markdownlint)
- 18 fix/verify scripts in `.opencode/fixes/`
