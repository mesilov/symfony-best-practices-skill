# Repository instructions

This repository maintains the `symfony-best-practices` Agent Skill.

For changes, reviews, PRs/MRs, or releases, use the local
[symfony-skill-maintainer](.agents/skills/symfony-skill-maintainer/SKILL.md) skill.
Its changelog gate applies before opening every PR, including drafts.

- `skills/symfony-best-practices/` is the distributable.
- `.agents/skills/symfony-skill-maintainer/` is repository-only.
- Preserve unrelated checkout work; use an isolated worktree when needed.
- Run the repository's validator, tests, build, and whitespace checks.
- Keep local checks, CI, merge, and release publication distinct in reports.
