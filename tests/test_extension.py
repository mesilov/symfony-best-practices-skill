"""Acceptance tests for two-source provenance and grouped routing."""
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/symfony-best-practices"


class ExtensionTests(unittest.TestCase):
    def test_two_sources_and_all_42_donors_are_present(self):
        manifest = json.loads((SKILL / "sources.json").read_text())
        self.assertEqual(3, manifest["schema_version"])
        self.assertEqual({"superpowers-symfony", "symfony-skills"}, {s["id"] for s in manifest["upstreams"]})
        self.assertEqual(42, len(manifest["donors"]))
        self.assertEqual(77, sum(len(d["files"]) for d in manifest["donors"]))
        migrations = [d for d in manifest["donors"] if d["name"] == "doctrine-migrations"]
        self.assertEqual(2, len(migrations))
        self.assertEqual(2, len({d["upstream"] for d in migrations}))

    def test_references_are_in_seven_complete_groups(self):
        groups = {p.name for p in (SKILL / "references").iterdir() if p.is_dir()}
        self.assertEqual({"workflow", "architecture", "http", "data", "async", "security", "presentation"}, groups)
        self.assertEqual(31, len(list((SKILL / "references").rglob("*.md"))))
        self.assertFalse(list((SKILL / "references").glob("*.md")))

    def test_new_source_corruption_is_rejected(self):
        mutations = ["missing_source", "unknown_source", "source_commit", "second_notice", "missing_template", "source_identity"]
        for mode in mutations:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                copied = Path(directory) / "symfony-best-practices"
                shutil.copytree(SKILL, copied)
                path = copied / "sources.json"
                manifest = json.loads(path.read_text())
                self.assertEqual(3, manifest["schema_version"], "Two-source provenance is not implemented")
                if mode == "missing_source": manifest["upstreams"].pop()
                elif mode == "unknown_source": manifest["donors"][-1]["upstream"] = "unknown"
                elif mode == "source_commit": manifest["upstreams"][1]["commit"] = "main"
                elif mode == "missing_template":
                    donor = next(d for d in manifest["donors"] if d["upstream"] == "symfony-skills" and d["name"] == "doctrine-orm")
                    donor["files"].pop()
                elif mode == "source_identity":
                    donor = next(d for d in manifest["donors"] if d["upstream"] == "symfony-skills" and d["name"] == "doctrine-migrations")
                    donor["upstream"] = "superpowers-symfony"
                elif mode == "second_notice":
                    notice = copied / "THIRD_PARTY_NOTICES.md"
                    notice.write_text(notice.read_text().replace("Faton Haliti", "Changed notice"))
                path.write_text(json.dumps(manifest))
                result = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), "--skill-dir", str(copied)], capture_output=True, text=True)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("ERROR", result.stdout + result.stderr)


if __name__ == "__main__": unittest.main()
