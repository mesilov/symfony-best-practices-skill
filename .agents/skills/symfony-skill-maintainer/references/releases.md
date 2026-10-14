# Preparing and publishing releases

Run from the repository root. Preparation, integration, tagging and publication are separate actions. Follow the user's authorized scope; a release request may authorize publication, while a repository edit or a request to prepare assets does not.

## Select the release tree and version

Inspect current remote branches, tags, releases and CI before choosing a target. Local branch lists or historical verification reports cannot establish current published state. Discover the repository from `git remote -v`; use the supported forge tools or authenticated CLI without exposing credentials.

Choose the intended full commit SHA and inspect its complete tree. If the default branch lacks the package, release from an explicitly selected complete tree or prepare the authorized integration. Enumerate accumulated branch changes before merging; do not silently include them under a version-only change. Follow existing tag naming, or make the chosen convention explicit when none exists.

The builder accepts a stable three-part `VERSION`; prerelease strings require a deliberate validator/builder change first. Choose a version consistent with the actual compatibility change. For a bump, update together:

- `VERSION`;
- product `SKILL.md` → `metadata.version`;
- `sources.json` → `skill_version`;
- current `SOURCES.md`, README version/archive names and changelog release entry;
- version-dependent tests, especially `tests/test_package.py`.

Current tests contain literal `0.1.0` archive names, a symlink-output fixture and a mutation based on `version: "0.1.0"`. Update all affected expectations; ensure the negative version still differs from the real one. Prefer deriving fixtures from `VERSION` when changing the tests. Preserve historical reports/design documents instead of globally replacing their old version strings. Add a new verification record and update README's current evidence link where appropriate.

Source review dates and framework baseline change only after actual review, independently of a release version bump. Repository-only maintainer edits do not change the distributed product version by themselves.

## Prepare a concrete candidate

Run [checks](checks.md), including source-byte verification where available; report any blocker or explicitly accepted exception. Commit the release files and record the candidate SHA. Build from a clean isolated checkout of the **final release SHA** after any integration, then verify again if its content differs from the tested candidate. Inspect terminal mandatory CI for that SHA before claiming CI success.

`scripts/build_release.py --output-dir /path/to/candidate` creates exactly the versioned `.tar.gz`, `.zip` and `SHA256SUMS`. Use a fresh directory and explicit filenames, so stale assets from another version cannot be uploaded. Prepare release notes describing behavior/coverage changes, compatibility, provenance and verification limits. The workflow currently uploads Actions artifacts; it does not create a GitHub Release.

## Publish within the authorized release task

Set `release_repo`, `release_version`, `release_tag`, `release_sha`, `release_assets` and `release_notes` to the inspected repository, selected version/tag, full SHA, fresh asset directory and saved notes file. Inspect existing remote tag/release first. Create and push a new annotated tag on that SHA only when the task authorizes it. Verify the remote tag resolves to that SHA, including peeling an annotated tag, before publication.

With GitHub CLI, inspect installed help for current flags. Once the exact remote tag exists:

```sh
gh release create "$release_tag" \
  "$release_assets/symfony-best-practices-$release_version.tar.gz" \
  "$release_assets/symfony-best-practices-$release_version.zip" \
  "$release_assets/SHA256SUMS" \
  --repo "$release_repo" --verify-tag \
  --title "Symfony Best Practices $release_version" \
  --notes-file "$release_notes"
```

`--verify-tag` prevents implicit tagging of the default branch. Use `--draft` when the request is for a draft; do not describe a draft as published. Set latest/prerelease behavior to the requested release policy, using installed help. No force-push or asset replacement is part of a normal new release.

After publication:

```sh
gh release view "$release_tag" --repo "$release_repo" \
  --json tagName,isDraft,isPrerelease,isImmutable,publishedAt,url,assets
gh release download "$release_tag" --repo "$release_repo" \
  --dir "$release_downloads" \
  --pattern "symfony-best-practices-$release_version.tar.gz" \
  --pattern "symfony-best-practices-$release_version.zip" \
  --pattern SHA256SUMS
```

Set `release_downloads` to a fresh directory. Check the exact expected asset names and sizes, then use the read-only asset verification command in [checks](checks.md) to compare archives and `SHA256SUMS` with the reviewed candidate and canonical tagged product. A checksum file alone is insufficient if it is not tied to the candidate. Record the release URL, tag target SHA, CI result and published digests; stop at the actually confirmed stage if readback/download fails.

## Existing tag or partial publication

If tag/release creation or upload has an unknown result, read back its state before retrying. Inspect tag target, draft/immutable state and attached assets. After a bounded corrective attempt, preserve receipts and report unresolved state instead of looping blindly.

When existing assets differ, preserve their names/digests and investigate tagged content, archive payloads and toolchain. Prefer a new corrected version for changed published content. A user-requested replacement is a separate operation: enumerate exact assets, reason and compatibility consequences, respect immutability, and verify replacement bytes. Do not erase historical failure evidence or silently move an existing tag.
