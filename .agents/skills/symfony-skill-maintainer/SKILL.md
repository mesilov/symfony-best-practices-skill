---
name: symfony-skill-maintainer
description: Use when maintaining the symfony-best-practices-skill repository, refreshing donor or official-documentation provenance, changing package checks, preparing pull/merge requests, or handling its releases.
license: MIT
---

# Symfony Skill Maintainer

Maintain this repository's **skill package**, using its actual scripts, source manifest and release evidence. For work inside a consuming Symfony application, use that application's instructions and the distributed `symfony-best-practices` skill.

## Establish repository context

Run `pwd`, `git status --short --branch`, `git worktree list` and `git remote -v`. Work from the repository root; inspect `AGENTS.md`, `README.md`, `VERSION`, `CHANGELOG.md`, `scripts/`, `tests/` and `.github/workflows/validate.yml` for the requested operation. Refresh remote state before delivery decisions.

Preserve unrelated changes. For new work, start from fresh `origin/main` on a `codex/` branch, using an isolated worktree when needed. When continuing, reviewing or publishing existing work, retain its branch/worktree and intended commits. Follow an explicitly requested alternative base; inspect the complete diff against the refreshed actual target before integration.

## Package boundaries

| Path | Responsibility |
| --- | --- |
| `skills/symfony-best-practices/` | Installable product: entrypoint, references, metadata, provenance and licenses |
| `.agents/skills/symfony-skill-maintainer/` | Canonical repository maintainer instructions and conditional procedures |
| `.codex/skills/`, `.claude/skills/` | Relative aliases to the canonical maintainer skill |
| `scripts/`, `tests/`, `.github/workflows/` | Offline validation, deterministic packaging and CI |
| `docs/` | Review decisions and dated verification evidence |

Keep agent instructions in English and preserve the current README's language and style. Keep the product entrypoint within the validator's word limit and load detail through thematic references. The maintainer skill is repository-only; adding it does not change the product version or archive contents.

## Changelog gate before every PR

Before opening any PR/MR, including drafts and documentation changes, commit a meaningful `CHANGELOG.md` entry for the actual change in the same branch. PR/MR mean GitHub pull requests here. Inspect its substantive diff against the refreshed target; recheck when scope or target changes. Follow the detailed gate in [checks](references/checks.md).

## Read the relevant procedure

- Source refresh, new coverage, version compatibility or licensing: [sources](references/sources.md).
- Repository edits, check failures and package acceptance: [checks](references/checks.md).
- Version bumps, tags, release assets or publication recovery: [releases](references/releases.md), then checks.

Do the preparation and checks covered by the request. Execute merge, push, tag or publication when authorized by the task; loading this skill grants no additional scope. Use existing authorization without repeatedly requesting it.

Report branch/base, changed scope, source revisions, executed checks and skipped or blocked checks. Distinguish local validation, source-byte verification, terminal CI, integration and published assets. Preserve historical evidence; append a dated record when the result changes.
