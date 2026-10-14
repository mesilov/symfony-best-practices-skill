"""Coverage and corruption checks for the official documentation review."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/symfony-best-practices"


class DocumentationTests(unittest.TestCase):
    def test_all_requested_pages_are_pinned_and_mapped(self):
        manifest = json.loads((SKILL / "sources.json").read_text())
        self.assertTrue("documentation" in manifest, "Official documentation coverage is missing")
        docs = manifest["documentation"]
        self.assertEqual("8.1", docs["framework_line"])
        self.assertEqual(40, len(docs["pages"]))
        urls = [url for page in docs["pages"] for url in page["requested_urls"]]
        self.assertEqual(43, len(urls))
        self.assertEqual(43, len(set(urls)))
        self.assertEqual({"symfony-docs", "symfony-ai"}, {r["id"] for r in docs["repositories"]})
        self.assertTrue(all(page["targets"] for page in docs["pages"]))
        self.assertEqual(31, len(list((SKILL / "references").rglob("*.md"))))

    def test_invalid_documentation_provenance_is_rejected(self):
        original = json.loads((SKILL / "sources.json").read_text())
        self.assertTrue("documentation" in original, "Official documentation coverage is missing")
        for mode in ["missing_page", "duplicate_url", "wrong_line", "bad_commit", "bad_hash", "path_escape", "missing_target", "missing_license", "missing_ai_notice", "corrupt_ai_notice", "missing_framework_attribution"]:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                copied = Path(directory) / "symfony-best-practices"
                shutil.copytree(SKILL, copied)
                manifest = json.loads((copied / "sources.json").read_text())
                docs = manifest["documentation"]
                if mode == "missing_page": docs["pages"].pop()
                elif mode == "duplicate_url": docs["pages"][-1]["requested_urls"] = docs["pages"][0]["requested_urls"]
                elif mode == "wrong_line": docs["framework_line"] = "8.0"
                elif mode == "bad_commit": docs["repositories"][0]["commit"] = "main"
                elif mode == "bad_hash": docs["pages"][0]["sha256"] = "bad"
                elif mode == "path_escape": docs["pages"][0]["path"] = "../../README.md"
                elif mode == "missing_target": docs["pages"][0]["targets"] = ["references/missing.md"]
                elif mode == "missing_license": docs["repositories"][0].pop("license")
                elif mode in {"missing_ai_notice", "corrupt_ai_notice", "missing_framework_attribution"}:
                    notice = copied / "THIRD_PARTY_NOTICES.md"
                    text = notice.read_text()
                    if mode == "missing_ai_notice": text = text.split("\n## symfony-ai\n")[0] + "\n"
                    elif mode == "corrupt_ai_notice": text = text.replace("Copyright (c) 2025-present Fabien Potencier", "Changed AI copyright")
                    else:
                        start, end = text.index("\n## Official documentation sources\n"), text.index("\n## symfony-ai\n")
                        text = text[:start] + text[end:]
                    notice.write_text(text)
                (copied / "sources.json").write_text(json.dumps(manifest))
                result = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), "--skill-dir", str(copied)], capture_output=True, text=True)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("ERROR", result.stdout + result.stderr)


if __name__ == "__main__": unittest.main()
