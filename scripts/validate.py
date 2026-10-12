#!/usr/bin/env python3
"""Validate the skill offline; optionally verify hashes against a pinned checkout."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/symfony-best-practices"
DONORS = set("bootstrap-check config-env-parameters controller-cleanup cqrs-and-handlers daily-workflow doctrine-batch-processing doctrine-fetch-modes doctrine-fixtures-foundry doctrine-migrations doctrine-relations doctrine-transactions e2e-panther-playwright effective-context form-types-validation functional-tests interfaces-and-autowiring messenger-retry-failures ports-and-adapters quality-checks rate-limiting strategy-pattern symfony-cache symfony-messenger symfony-scheduler symfony-voters tdd-with-phpunit test-doubles-mocking twig-components value-objects-and-dtos".split())
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def validate(skill_dir=SKILL, upstream_dir=None):
    skill_dir = Path(skill_dir).absolute()
    version = (ROOT / "VERSION").read_text().strip()
    errors = []

    def require(condition, message):
        if not condition: errors.append(message)

    def read(name):
        path = skill_dir / name
        if not path.is_file():
            errors.append(f"Missing file: {name}")
            return ""
        return path.read_text(encoding="utf-8")

    require(bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "VERSION must be a stable semver")
    if not skill_dir.is_dir(): return [f"Missing skill directory: {skill_dir}"]
    symlinks = [p for p in skill_dir.rglob("*") if p.is_symlink()]
    if skill_dir.is_symlink() or symlinks:
        return ["Symlinks are not allowed in the distributable skill"]
    allowed_roots = {"SKILL.md", "LICENSE", "THIRD_PARTY_NOTICES.md", "SOURCES.md", "sources.json"}
    for path in skill_dir.rglob("*"):
        if path.is_file():
            relative = path.relative_to(skill_dir)
            require(relative.as_posix() in allowed_roots or (relative.parts[0] == "references" and path.suffix == ".md") or relative.as_posix() == "agents/openai.yaml", f"Unexpected package file: {relative}")

    skill_text = read("SKILL.md")
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", skill_text, re.S)
    require(match is not None, "SKILL.md needs YAML frontmatter and a body")
    if not match: return errors
    try:
        front = yaml.safe_load(match[1])
        require(isinstance(front, dict), "Frontmatter must be a mapping")
        if not isinstance(front, dict): return errors
        require(set(front) <= {"name", "description", "license", "metadata", "compatibility", "allowed-tools"}, "Unsupported skill frontmatter keys")
        require(front.get("name") == "symfony-best-practices", "Invalid skill name")
        require(skill_dir.name == front.get("name"), "Skill folder must match its name")
        description = front.get("description")
        require(isinstance(description, str) and 0 < len(description) <= 1024, "Invalid description")
        require(front.get("license") == "MIT", "Skill license must be MIT")
        require(isinstance(front.get("metadata"), dict) and front["metadata"].get("version") == version, "Skill metadata version does not match VERSION")
        require(len(match[2].split()) <= 500, "Skill entry body exceeds 500 words")
    except yaml.YAMLError as exc:
        return errors + [f"Invalid frontmatter YAML: {exc}"]

    for path in skill_dir.rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        require(not re.search(r"\b(?:TODO|TBD|FIXME)\b|\[INSERT", content), f"Unfinished content: {path.relative_to(skill_dir)}")
        require(sum(line.startswith("```") for line in content.splitlines()) % 2 == 0, f"Unclosed code fence: {path.name}")
        for target in LINK.findall(content):
            parsed = urlsplit(target)
            if parsed.scheme in {"https", "http", "mailto"}: continue
            require(not parsed.scheme and not parsed.netloc, f"Unsupported link: {target}")
            if not parsed.path: continue
            linked = (path.parent / unquote(parsed.path)).resolve()
            if not linked.is_relative_to(skill_dir.resolve()):
                errors.append(f"Link escapes skill: {path.name}: {target}")
                continue
            require(linked.is_file(), f"Broken local link: {path.name}: {target}")
            if parsed.fragment and linked.is_file() and linked.suffix == ".md":
                headings = re.findall(r"^#+\s+(.+)$", linked.read_text(), re.M)
                anchors = {re.sub(r"[^\w-]", "", h.lower().replace(" ", "-")) for h in headings}
                require(unquote(parsed.fragment) in anchors, f"Broken heading link: {target}")

    references = {p.relative_to(skill_dir).as_posix() for p in (skill_dir / "references").glob("*.md")}
    require(len(references) == 12, "Expected 12 thematic references")
    routed = {t for t in LINK.findall(match[2]) if t.startswith("references/")}
    require(references == routed, "SKILL.md routing must cover every reference")
    try:
        interface = yaml.safe_load(read("agents/openai.yaml"))
        require(isinstance(interface, dict), "UI metadata must be a mapping")
        if isinstance(interface, dict):
            values = interface.get("interface", {})
            require(isinstance(values, dict), "UI interface must be a mapping")
            if isinstance(values, dict):
                require(isinstance(values.get("display_name"), str), "Missing display name")
                blurb = values.get("short_description")
                require(isinstance(blurb, str) and 25 <= len(blurb) <= 64, "UI short_description must be 25-64 characters")
                prompt = values.get("default_prompt", "")
                require(isinstance(prompt, str) and "$symfony-best-practices" in prompt, "Default prompt must invoke the skill")
            policy = interface.get("policy", {})
            require(isinstance(policy, dict) and policy.get("allow_implicit_invocation", True) is True, "Implicit invocation should remain enabled")
    except yaml.YAMLError as exc: errors.append(f"Invalid UI YAML: {exc}")

    own_license = read("LICENSE")
    require(own_license == (ROOT / "LICENSE").read_text(), "Package license must preserve project LICENSE")
    notices = read("THIRD_PARTY_NOTICES.md")
    read("SOURCES.md")
    try:
        manifest = json.loads(read("sources.json"))
        if not isinstance(manifest, dict): return errors + ["sources.json must be an object"]
        require(manifest.get("schema_version") == 1, "Invalid provenance schema version")
        require(manifest.get("skill_version") == version, "Provenance version does not match VERSION")
        upstream = manifest.get("upstream", {})
        donors = manifest.get("donors", [])
        if not isinstance(upstream, dict) or not isinstance(donors, list): return errors + ["Invalid provenance structure"]
        commit = upstream.get("commit", "")
        require(isinstance(commit, str) and bool(HEX40.fullmatch(commit)), "Upstream commit must be a full SHA")
        repository = "https://github.com/dev-toolings/superpowers-symfony"
        require(upstream.get("repository") == repository, "Unexpected donor repository")
        names = [d.get("name") for d in donors if isinstance(d, dict)]
        require(len(donors) == 29 and len(names) == 29 and set(names) == DONORS and len(set(names)) == 29, "Expected exactly the selected 29 distinct donors")
        targets = set()
        for donor in donors:
            if not isinstance(donor, dict): errors.append("Donor must be an object"); continue
            name = donor.get("name", "")
            files = donor.get("files", [])
            selected = donor.get("targets", [])
            require(isinstance(selected, list) and bool(selected) and all(t in references for t in selected), f"Invalid targets for {name}")
            if isinstance(selected, list): targets.update(t for t in selected if isinstance(t, str))
            expected = {f"content/skills/{name}/SKILL.md", f"content/skills/{name}/reference.md"}
            require(isinstance(files, list) and len(files) == 2 and {f.get("path") for f in files if isinstance(f, dict)} == expected, f"Missing source files for {name}")
            require(donor.get("source_url") == f"{repository}/tree/{commit}/content/skills/{name}", f"Source URL is not pinned for {name}")
            if name == "symfony-scheduler": require(donor.get("requested_path") == "content/skills/symfony-schedu", "Scheduler path correction must be explicit")
            for source in files if isinstance(files, list) else []:
                if not isinstance(source, dict): errors.append(f"Invalid source entry for {name}"); continue
                digest = source.get("sha256", "")
                require(isinstance(digest, str) and bool(HEX64.fullmatch(digest)), f"Invalid SHA-256 for {name}")
                if upstream_dir and source.get("path") in expected:
                    origin = Path(upstream_dir) / source["path"]
                    require(origin.is_file() and hashlib.sha256(origin.read_bytes()).hexdigest() == digest, f"Upstream hash mismatch: {source['path']}")
        require(targets == references, "Donor map must cover every thematic reference")
        license_info = upstream.get("license", {})
        if not isinstance(license_info, dict): return errors + ["Invalid upstream license entry"]
        digest = license_info.get("sha256", "")
        require(license_info.get("path") == "LICENSE" and isinstance(digest, str) and bool(HEX64.fullmatch(digest)), "Invalid upstream license provenance")
        marker = "The following notice is reproduced in full:\n\n"
        require(marker in notices, "Full upstream license notice missing")
        if marker in notices:
            require(hashlib.sha256(notices.split(marker, 1)[1].encode()).hexdigest() == digest, "Full upstream LICENSE must be preserved byte-for-byte")
        if upstream_dir:
            origin = Path(upstream_dir) / "LICENSE"
            require(origin.is_file() and hashlib.sha256(origin.read_bytes()).hexdigest() == digest, "Upstream LICENSE hash mismatch")
            result = subprocess.run(["git", "-C", str(upstream_dir), "rev-parse", "HEAD"], capture_output=True, text=True)
            require(result.returncode == 0 and result.stdout.strip() == commit, "Upstream checkout does not match pinned commit")
    except (ValueError, TypeError, KeyError) as exc: errors.append(f"Invalid provenance JSON/structure: {exc}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", type=Path, default=SKILL)
    parser.add_argument("--upstream-dir", type=Path, help="Optional donor checkout for actual SHA/hash comparison")
    args = parser.parse_args()
    try: errors = validate(args.skill_dir, args.upstream_dir)
    except (OSError, UnicodeError) as exc: errors = [str(exc)]
    if errors:
        for error in errors: print(f"ERROR: {error}")
        return 1
    print(f"OK: symfony-best-practices {(ROOT / 'VERSION').read_text().strip()}; 12 references; 29 donors / 58 source files")
    return 0


if __name__ == "__main__": sys.exit(main())
