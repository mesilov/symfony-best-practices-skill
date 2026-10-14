"""Offline provenance rules for the complete selected official-documentation set."""
from pathlib import Path
import hashlib
import re
import subprocess

SLUGS = set("routing controller templates configuration components/http_kernel reference/configuration/kernel service_container event_dispatcher doctrine forms testing session cache logging controller/error_pages console mailer validation messenger scheduler notifier serializer translation security security/passwords security/csrf http_client components/filesystem expression_language lock workflow components/uid components/yaml webhook deployment performance http_cache ai/components/mate ai/bundles/mcp-bundle ai/bundles/ai-bundle".split())
REPOSITORIES = {
    "symfony-docs": ("https://github.com/symfony/symfony-docs", "8.1", "LICENSE.md", "CC-BY-SA-3.0"),
    "symfony-ai": ("https://github.com/symfony/ai", "main", "LICENSE", "MIT"),
}
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")


def validate_documentation(documentation, references, checkouts, notices, require):
    """Append actionable errors and return the validly shaped coverage set."""
    targets = set()
    if not isinstance(documentation, dict):
        require(False, "Official documentation provenance must be an object")
        return targets
    require(documentation.get("framework_line") == "8.1", "Official documentation baseline must be 8.1")
    require(documentation.get("reviewed_on") == "2026-10-15", "Official documentation review date mismatch")
    repositories, pages = documentation.get("repositories"), documentation.get("pages")
    if not isinstance(repositories, list) or not isinstance(pages, list):
        require(False, "Invalid official documentation repositories/pages")
        return targets
    records = {r.get("id"): r for r in repositories if isinstance(r, dict) and isinstance(r.get("id"), str)}
    require(len(repositories) == 2 and set(records) == set(REPOSITORIES), "Expected two distinct official documentation repositories")
    require(set(checkouts) <= set(REPOSITORIES), "Unknown documentation checkout ID")
    for source_id, record in records.items():
        if source_id not in REPOSITORIES: continue
        repository, revision, license_path, identifier = REPOSITORIES[source_id]
        commit = record.get("commit", "")
        require(record.get("repository") == repository and record.get("revision") == revision, f"Unexpected documentation repository/revision: {source_id}")
        require(isinstance(commit, str) and bool(HEX40.fullmatch(commit)), f"Documentation commit must be a full SHA: {source_id}")
        license_info = record.get("license")
        if not isinstance(license_info, dict):
            require(False, f"Missing documentation license: {source_id}")
            continue
        digest = license_info.get("sha256", "")
        require(license_info.get("path") == license_path and license_info.get("identifier") == identifier and isinstance(digest, str) and bool(HEX64.fullmatch(digest)), f"Invalid documentation license: {source_id}")
        if source_id == "symfony-ai":
            section = re.search(r"^## symfony-ai\n.*?^```text\n(.*?)^```$", notices, re.M | re.S)
            require(section is not None, "Full official symfony-ai license notice missing")
            if section: require(hashlib.sha256(section[1].encode()).hexdigest() == digest, "Official symfony-ai LICENSE must be preserved verbatim")
        else:
            section = re.search(r"^## Official documentation sources\n(.*?)(?=^## |\Z)", notices, re.M | re.S)
            attribution = section[1] if section else ""
            require("Symfony Docs contributors" in attribution and "https://creativecommons.org/licenses/by-sa/3.0/" in attribution and f"{repository}/blob/{commit}/{license_path}" in attribution, "Official Symfony Docs attribution/license link missing")
        if source_id in checkouts:
            checkout = Path(checkouts[source_id])
            origin = checkout / license_path
            require(origin.is_file() and hashlib.sha256(origin.read_bytes()).hexdigest() == digest, f"Documentation LICENSE hash mismatch: {source_id}")
            result = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"], capture_output=True, text=True)
            require(result.returncode == 0 and result.stdout.strip() == commit, f"Documentation checkout does not match pinned SHA: {source_id}")
    identities = [p.get("id") for p in pages if isinstance(p, dict) and isinstance(p.get("id"), str)]
    require(len(pages) == 40 and len(identities) == 40 and set(identities) == SLUGS, "Expected exactly the 40 selected official documents")
    requested_urls = []
    for page in pages:
        if not isinstance(page, dict):
            require(False, "Documentation page must be an object")
            continue
        slug = page.get("id")
        if not isinstance(slug, str) or slug not in SLUGS:
            require(False, "Unknown documentation page identity")
            continue
        source_id = "symfony-ai" if slug.startswith("ai/") else "symfony-docs"
        path = "docs/" + slug.removeprefix("ai/") + ".rst" if source_id == "symfony-ai" else slug + ".rst"
        require(page.get("repository") == source_id and page.get("path") == path, f"Unexpected documentation source path: {slug}")
        digest = page.get("sha256", "")
        require(isinstance(digest, str) and bool(HEX64.fullmatch(digest)), f"Invalid documentation SHA-256: {slug}")
        record = records.get(source_id, {})
        require(page.get("source_url") == f"{REPOSITORIES[source_id][0]}/blob/{record.get('commit')}/{path}", f"Documentation source URL must be pinned: {slug}")
        url = f"https://symfony.com/doc/current/{slug}.html"
        expected = [url]
        if slug == "security": expected += [url + "#" + anchor for anchor in ["the-user", "the-firewall", "access-control-authorization"]]
        selected_urls = page.get("requested_urls")
        require(selected_urls == expected, f"Requested documentation URLs mismatch: {slug}")
        if isinstance(selected_urls, list): requested_urls += [u for u in selected_urls if isinstance(u, str)]
        selected = page.get("targets")
        require(isinstance(selected, list) and bool(selected) and all(isinstance(t, str) and t in references for t in selected), f"Invalid documentation targets: {slug}")
        if isinstance(selected, list): targets.update(t for t in selected if isinstance(t, str))
        if source_id in checkouts and page.get("path") == path:
            origin = Path(checkouts[source_id]) / path
            require(origin.is_file() and hashlib.sha256(origin.read_bytes()).hexdigest() == digest, f"Documentation source hash mismatch: {slug}")
    require(len(requested_urls) == 43 and len(set(requested_urls)) == 43, "Expected all 43 distinct requested documentation URLs")
    return targets
