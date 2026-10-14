# Maintainer Skill Implementation Plan

**Goal:** Add repository-local guidance for maintenance, source refresh, validation and releases.

**Architecture:** One canonical skill under `.agents/skills/symfony-skill-maintainer`, three conditional references and relative aliases. The distributable remains `skills/symfony-best-practices/`.

**Tech stack:** Markdown, YAML, Python unittest and the existing package scripts.

## 1. Establish baseline

- [x] Create an isolated worktree on `codex/add-project-maintainer` from `81fa983`, then rebase the maintainer commit onto updated `origin/main` at `54c7b20`.
- [x] Run `python -B -m unittest discover -s tests -v` and `scripts/validate.py` with both `--upstream` and both `--docs-checkout` selections.
- [x] Add `tests/test_maintainer.py` checking frontmatter/UI discovery, reference reachability and relative aliases. Run `python -B -m unittest discover -s tests -p test_maintainer.py -v`; expect failures for missing skill and aliases.
- [x] Dispatch a read-only baseline assessment using three realistic source/release requests and raw repository files, without the proposed answers.

## 2. Write and expose the skill

- [x] Create `.agents/skills/symfony-skill-maintainer/SKILL.md` and `agents/openai.yaml` with automatic discovery and an explicit `$symfony-skill-maintainer` default prompt.
- [x] Add `references/sources.md`, `checks.md` and `releases.md`, with commands verified against existing scripts and installed GitHub CLI help.
- [x] Add relative aliases `.codex/skills/symfony-skill-maintainer` and `.claude/skills/symfony-skill-maintainer`, both targeting `../../.agents/skills/symfony-skill-maintainer`.
- [x] Add root `AGENTS.md` routing repository maintenance to the local skill. Update README and an Unreleased changelog entry without changing the product version.

## 3. Verify and record

- [x] Run the new structural tests, full unittest discovery, pinned-source validator and skill-creator `quick_validate.py` for both skills.
- [x] Build archives with `scripts/build_release.py`; existing reproducibility tests compare tar/zip/checksum bytes and canonical members.
- [x] Repeat the same three requests with the skill in a fresh read-only agent; fix only demonstrated gaps. Add and exercise the missing read-only asset verification command; obtain a focused recheck.
- [x] Record commands, counts, scenario limits and worktree/base in `docs/verification-maintainer-2026-10-15.md`. Preserve older evidence.
- [x] Run `git diff --check`, inspect scope and commit only this maintainer change locally.

Execution stays in this chat. No merge, push, tag or GitHub Release is part of adding the skill.
