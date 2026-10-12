"""Behavioral checks for the distributable skill and its release commands."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/symfony-best-practices"


def run(script, *args):
    return subprocess.run([sys.executable, str(ROOT / "scripts" / script), *map(str, args)], capture_output=True, text=True)


class PackageTests(unittest.TestCase):
    def test_repository_validates(self):
        result = run("validate.py")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_release_builds(self):
        with tempfile.TemporaryDirectory() as directory:
            result = run("build_release.py", "--output-dir", directory)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual({"symfony-best-practices-0.1.0.tar.gz", "symfony-best-practices-0.1.0.zip", "SHA256SUMS"}, {p.name for p in Path(directory).iterdir()})

    def test_invalid_package_is_rejected(self):
        if not SKILL.exists():
            self.fail("The canonical skill is missing")
        changes = [
            ("version mismatch", "SKILL.md", lambda s: s.replace('version: "0.1.0"', 'version: "0.2.0"')),
            ("missing reference", "references/cache.md", None),
            ("broken link", "SKILL.md", lambda s: s + "\n[missing](references/absent.md)\n"),
            ("path escape", "SKILL.md", lambda s: s + "\n[escape](../../README.md)\n"),
            ("missing license", "THIRD_PARTY_NOTICES.md", None),
            ("corrupt notice", "THIRD_PARTY_NOTICES.md", lambda s: s.replace("Copyright (c) 2024", "Copyright (c) 2025")),
            ("invalid yaml", "SKILL.md", lambda s: s.replace("name: symfony-best-practices", "name: [unclosed")),
            ("unsupported frontmatter", "SKILL.md", lambda s: s.replace("license: MIT", "capabilities: [read]\nlicense: MIT")),
            ("disabled discovery", "agents/openai.yaml", lambda s: s + "\npolicy:\n  allow_implicit_invocation: false\n"),
            ("invalid UI prompt", "agents/openai.yaml", lambda s: s.replace("$symfony-best-practices", "a different tool")),
            ("invalid manifest version", "sources.json", lambda s: self.change_manifest(s, "version")),
            ("placeholder", "references/cache.md", lambda s: s + "\nTODO: finish this section\n"),
            ("missing donor", "sources.json", lambda s: self.change_manifest(s, "missing")),
            ("duplicate donor", "sources.json", lambda s: self.change_manifest(s, "duplicate")),
            ("invalid upstream sha", "sources.json", lambda s: self.change_manifest(s, "sha")),
            ("invalid source hash", "sources.json", lambda s: self.change_manifest(s, "hash")),
            ("missing source file", "sources.json", lambda s: self.change_manifest(s, "file")),
            ("missing target", "sources.json", lambda s: self.change_manifest(s, "target")),
        ]
        for label, name, transform in changes:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                copied = Path(directory) / "symfony-best-practices"
                shutil.copytree(SKILL, copied)
                path = copied / name
                if transform is None:
                    path.unlink()
                else:
                    path.write_text(transform(path.read_text()))
                result = run("validate.py", "--skill-dir", copied)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)
                self.assertIn("ERROR", result.stdout + result.stderr)

    @staticmethod
    def change_manifest(text, mode):
        value = json.loads(text)
        if mode == "version": value["skill_version"] = "0.2.0"
        elif mode == "missing": value["donors"].pop()
        elif mode == "duplicate": value["donors"][-1] = value["donors"][0]
        elif mode == "sha": value["upstream"]["commit"] = "main"
        elif mode == "hash": value["donors"][0]["files"][0]["sha256"] = "bad"
        elif mode == "file": value["donors"][0]["files"].pop()
        elif mode == "target": value["donors"][0]["targets"] = ["references/absent.md"]
        return json.dumps(value)

    def test_unexpected_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "symfony-best-practices"
            shutil.copytree(SKILL, copied)
            (copied / "credentials.env").write_text("FAKE_TOKEN=not-a-secret\n")
            result = run("validate.py", "--skill-dir", copied)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_output_cannot_be_inside_skill(self):
        result = run("build_release.py", "--output-dir", SKILL / "dist")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertFalse((SKILL / "dist").exists())

    def test_existing_symlink_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            external = Path(directory) / "original.txt"
            external.write_text("must not change")
            (Path(directory) / "symfony-best-practices-0.1.0.tar.gz").symlink_to(external)
            result = run("build_release.py", "--output-dir", directory)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertEqual("must not change", external.read_text())

    def test_symlink_is_rejected(self):
        if not SKILL.exists(): self.fail("The canonical skill is missing")
        with tempfile.TemporaryDirectory() as directory:
            copied = Path(directory) / "symfony-best-practices"
            shutil.copytree(SKILL, copied)
            (copied / "escape.md").symlink_to(ROOT / "README.md")
            result = run("validate.py", "--skill-dir", copied)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_archives_are_complete_and_reproducible(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            for directory in [first, second]:
                result = run("build_release.py", "--output-dir", directory)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            for artifact in Path(first).iterdir():
                self.assertEqual(artifact.read_bytes(), (Path(second) / artifact.name).read_bytes(), artifact.name)
            expected = {"symfony-best-practices/" + p.relative_to(SKILL).as_posix() for p in SKILL.rglob("*") if p.is_file()}
            with tarfile.open(Path(first) / "symfony-best-practices-0.1.0.tar.gz") as archive:
                self.assertEqual(expected, {m.name for m in archive.getmembers() if m.isfile()})
                for member in archive.getmembers():
                    if member.isfile(): self.assertEqual((SKILL / member.name.split("/", 1)[1]).read_bytes(), archive.extractfile(member).read())
            with zipfile.ZipFile(Path(first) / "symfony-best-practices-0.1.0.zip") as archive:
                self.assertEqual(expected, set(archive.namelist()))
                for name in archive.namelist(): self.assertEqual((SKILL / name.split("/", 1)[1]).read_bytes(), archive.read(name))
            for line in (Path(first) / "SHA256SUMS").read_text().splitlines():
                digest, name = line.split("  ")
                self.assertEqual(digest, hashlib.sha256((Path(first) / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
