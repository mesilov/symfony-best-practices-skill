# Repository checks

Run from the repository root. This is a Python-backed documentation package, not a Symfony runtime application. Read current scripts and CI before using these commands; `--help` documents supported flags.

## Changelog gate before every PR

Before opening any PR/MR, commit a meaningful `CHANGELOG.md` update in the same branch. This applies to drafts and to documentation, tests, skills, build tools, fixes and small changes. Describe the actual change and its effect under `Unreleased`, following the file's format. For a release, move accumulated entries into the version section rather than inventing a change.

Refresh the actual target. Inspect both changelog text and its substantive target-to-head diff. An entry already in the target, unrelated history, whitespace, deletion alone or a promise to add notes later does not satisfy the gate. Add a truthful entry and commit it before opening; if the change cannot be described truthfully, stop PR creation and explain the unresolved point. Avoid filler and duplicated history. Recheck after scope or target changes.

When opening a PR is authorized, push the existing requested branch and target `main` unless another base was requested. Read back its base, head SHA, changed scope, changelog and CI; PR creation does not authorize merge, tags or release publication.

## Environment and standard gates

Python 3.11+ and the pinned `requirements-dev.txt` dependency are used by CI. Reuse an existing suitable environment or create a local one:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -B scripts/validate.py
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B scripts/build_release.py
git diff --check
```

On Windows use `.venv\Scripts\python.exe`. Record the actual Python/PyYAML versions and executable used. `ModuleNotFoundError: yaml` means the selected environment lacks the required dependency; switch to or prepare the declared environment before judging the package.

`validate.py` covers the distributed product, not the repository-only maintainer skill. `tests/test_maintainer.py`, included by ordinary unittest discovery in CI, checks its frontmatter/UI, reference reachability and canonical relative aliases. If skill-creator is available, also run its `scripts/quick_validate.py` on both skill directories; its presence is not a portable repository requirement.

For source changes and release candidates, also perform [pinned-checkout validation](sources.md). Record explicitly any unavailable checkout; plain offline `OK` has narrower meaning.

## What each gate proves

| Gate | Evidence |
| --- | --- |
| Product validator | Version agreement, routing, manifest shape/coverage and notice integrity |
| Checkout flags | Supplied source HEAD and raw-file/license hashes match recorded pins |
| Unit tests | Valid package, rejection of corrupt provenance and unsafe output, archive completeness and reproducibility; maintainer discovery/links |
| Builder | Local `.tar.gz`, `.zip`, `SHA256SUMS` created from the canonical product directory |
| CI | Those jobs finished for the inspected remote SHA and configuration |

## Packaging and behavioral review

The builder packages only `skills/symfony-best-practices/`, with top-level archive folder `symfony-best-practices/`. Repository instructions, aliases, scripts/tests, reviews, credentials and unrelated generated files do not belong in the payload. Keep symlinks out of the product; repository skill aliases live outside it.

The archive tests compare every member with canonical bytes, verify checksum entries, and compare two builds in one toolchain. Check the actual release candidate as well when preparing publication. Reproducibility in one Python/zlib environment does not promise identical compressed bytes in every toolchain; compare payloads and record the toolchain when investigating a discrepancy.

To check downloaded assets against a reviewed candidate, run the following from a clean checkout of the final release SHA. Set `release_downloads` to the downloaded directory and `release_assets` to the candidate directory. For a local candidate check, pass its directory in both positions. The command only reads files:

```sh
.venv/bin/python -B - "$release_downloads" "$release_assets" <<'PY'
from pathlib import Path
import hashlib
import tarfile
import sys
import zipfile

downloaded, candidate = map(Path, sys.argv[1:])
version = Path("VERSION").read_text().strip()
names = {f"symfony-best-practices-{version}.{suffix}" for suffix in ("tar.gz", "zip")}
sums = {}
for line in (downloaded / "SHA256SUMS").read_text().splitlines():
    digest, name = line.split("  ", 1)
    assert name not in sums, "Duplicate checksum entry"
    sums[name] = digest
assert set(sums) == names, "Unexpected checksum filenames"
for name in names:
    payload = (downloaded / name).read_bytes()
    assert hashlib.sha256(payload).hexdigest() == sums[name], name
    assert payload == (candidate / name).read_bytes(), f"Candidate bytes differ: {name}"
assert (downloaded / "SHA256SUMS").read_bytes() == (candidate / "SHA256SUMS").read_bytes()
product = Path("skills/symfony-best-practices")
expected = {"symfony-best-practices/" + p.relative_to(product).as_posix(): p.read_bytes()
            for p in product.rglob("*") if p.is_file()}
with tarfile.open(downloaded / f"symfony-best-practices-{version}.tar.gz") as archive:
    members = archive.getmembers()
    assert len(members) == len(expected) and {m.name for m in members} == set(expected)
    assert all(m.isfile() and m.size == len(expected[m.name]) for m in members)
    assert {m.name: archive.extractfile(m).read() for m in members} == expected
with zipfile.ZipFile(downloaded / f"symfony-best-practices-{version}.zip") as archive:
    members = archive.infolist()
    assert len(members) == len(expected) and {m.filename for m in members} == set(expected)
    assert all(m.file_size == len(expected[m.filename]) for m in members)
    assert {m.filename: archive.read(m) for m in members} == expected
print(f"OK: both archives, {len(expected)} canonical files, candidate bytes and checksums")
PY
```

This establishes asset integrity and candidate agreement; the preceding remote tag/CI readback still establishes the release identity.

For substantial guidance changes, use affected cases from `tests/scenarios.md`. For this maintainer skill use `tests/maintainer-scenarios.md`. A fresh read-only agent may apply the skill to the request with only relevant raw artifacts. Assess its decisions and referenced procedures, preserve demonstrated gaps, and avoid claiming quantified behavioral improvement without evidence. Textual scenarios do not prove real Symfony, DB, broker or provider behavior.

When a required check fails, inspect the failure and affected implementation; preserve unrelated work. For changed executable behavior, add a meaningful regression and observe its failure before fixing. Do not weaken an acceptance constraint to make an unexplained result green.

Record a dated verification report under `docs/` with commands, counts, versions, branch/base, source-check coverage and limitations. Existing reports remain historical. For a remote delivery, inspect terminal CI on the exact candidate SHA; uploaded Actions artifacts are separate from a published release.
