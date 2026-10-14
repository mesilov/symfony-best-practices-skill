# Updating sources and coverage

Run commands from the repository root. Start with `skills/symfony-best-practices/sources.json`, `SOURCES.md`, `THIRD_PARTY_NOTICES.md`, `docs/source-review.md` and the relevant official-documentation review. The manifest identifies the selected sources; it is not a claim that upstream HEAD is current.

## Select and review revisions

The repository currently records two donor repositories (`superpowers-symfony`, `symfony-skills`) and two official repositories (`symfony-docs`, `symfony-ai`). Use their manifest URLs and revisions instead of remembered checkout paths or floating `/current/` documentation alone.

Obtain clean, separate checkouts when source verification is needed. Compare old and candidate commits, inspect relevant files and license changes, then pin full commit SHAs. A branch name is a selection aid; record the actual SHA. Do not reset a user's existing source checkout. Refresh only the sources requested or affected, and report sources deliberately left pinned.

Donor identity is `(upstream, name)`: the two `doctrine-migrations` records remain separate even when they target one reference. Preserve the explicit Scheduler requested-path correction. Changes in selected donors, file paths, groups or documentation coverage require deliberate changes to the validator's expected sets and regression fixtures.

## Update one coherent change

1. Review API facts against the selected framework minor and separately versioned Doctrine, Foundry, UX, Lexik and Symfony AI packages. Retain compatibility notes when the distributed target remains Symfony 8.x.
2. Update affected English references with original guidance, conditional architecture choices and usable primary-source links. Maintain the short product entrypoint and its full routing.
3. Update manifest commits, commit-pinned URLs, SHA-256 of **raw source bytes**, license paths/hashes, review dates and donor/page targets. Retained records must also point to the selected revision. Do not derive hashes from rendered HTML or adapted guidance.
4. Update `SOURCES.md`, notices, the review document, README coverage and changelog where affected. Preserve complete donor and Symfony AI MIT notices. Symfony Docs attribution and CC BY-SA 3.0 links remain explicit; copying manual prose or examples would require a separate license decision from the current original-synthesis approach.
5. Inspect `scripts/validate.py`, `scripts/documentation.py` and relevant tests. At the current baseline these enforce schema 3, 31 references, 42 donors, 77 donor files, 40 documentation pages / 43 requested URLs, framework line 8.1 and documentation review date 2026-10-15. These are maintained acceptance constraints, not timeless facts. Update them together when the accepted baseline changes; do not remove checks just to accept an unexplained mismatch.

Security anchors share one source page. Preserve each requested URL and its mapping even when multiple URLs have the same raw-file hash.

## Verify recorded bytes

Replace the example paths with clean checkouts at the **manifest commits**. Use the Python environment from [checks](checks.md):

```sh
.venv/bin/python -B scripts/validate.py \
  --upstream superpowers-symfony=/path/to/superpowers-symfony \
  --upstream symfony-skills=/path/to/symfony-skills \
  --docs-checkout symfony-docs=/path/to/symfony-docs \
  --docs-checkout symfony-ai=/path/to/symfony-ai
```

Each supplied checkout validates that source's HEAD, selected files and license. All four selections are required to claim verification of all recorded sources. Default offline validation checks structure, coverage and bundled notices; omitted checkout flags do not fail and do not prove source bytes or freshness. No automatic source-refresh command exists in this repository.

Run [checks](checks.md) and source-related regression scenarios after adaptation. Record selected revisions, material differences, coverage changes and unresolved compatibility questions. If retrieval is blocked, preserve existing provenance and report the missing source check rather than recording invented hashes or a new review date.
