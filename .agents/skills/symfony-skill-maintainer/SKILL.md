---
name: symfony-skill-maintainer
description: Use when maintaining the symfony-best-practices-skill repository, changing its skills, sources, documentation or build tools, preparing a pull/merge request, or handling a release.
license: MIT
---

# Symfony Skill Maintainer

Maintain this repository and its distributable skill. This maintainer skill is repository-only; keep it outside `skills/symfony-best-practices/` and release archives. Here, MR and PR both mean a GitHub pull request.

## Establish context

Read [AGENTS.md](../../../AGENTS.md), the requested scope, Git status, remotes, and current branches. Preserve unrelated changes. Start from fresh `origin/main` on a `codex/` branch, using an isolated worktree when needed. Follow an explicitly requested alternative base.

The distributable lives in `skills/symfony-best-practices/`. Validation/build tools live in `scripts/`; package tests and decision scenarios live in `tests/`. Use the project's Python environment and pinned development dependencies.

Keep `VERSION`, skill metadata, provenance, license notices, links, and release names consistent when changing the package. Apply architecture/API guidance in the distributable only to tasks in its scope.

## Changelog gate before every PR

**Before opening any PR/MR, commit a meaningful [CHANGELOG.md](../../../CHANGELOG.md) update in the same branch.** This applies to draft PRs and to documentation, tests, skills, build tools, fixes, and small changes.

Describe the actual change and its effect. Add it under `Unreleased`, following the file's format. For a release, move the accumulated entries into the appropriate version section instead of inventing a new change.

Refresh the actual target branch. Inspect both the changelog text and its substantive diff against that branch. An existing entry already in the target, an unrelated entry, whitespace, deletion alone, or a promise to add notes later does not satisfy this gate.

If the entry is missing, add it and commit it before opening the PR. If a truthful entry cannot be written, stop PR creation and explain the unresolved point. Do not invent filler or duplicate history to produce a diff.

Example: `Add repository maintainer guidance that requires changelog entries before opening any PR.`

## Validate and deliver

From the repository root, run through the selected Python environment:

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/build_release.py
git diff --check
```

For changed skills, use an available skill validator and focused decision scenarios. Confirm that archives contain only the distributable. Check staged/new files as well as tracked differences.

When PR creation is authorized, push the branch and open it against `main` unless another target was requested. Check its base, head commit, scope, changelog, and CI. Recheck the gate after scope or target changes.

A PR request does not authorize merge, tags, or releases. Perform those only within the user's authorization. Report confirmed links, commits, checks, and remaining limits. Distinguish local validation, CI, merge, and published release evidence.
