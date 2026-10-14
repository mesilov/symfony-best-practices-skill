"""Check discovery and local-reference integrity of the repository-only skill."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
NAME = "symfony-skill-maintainer"
SKILL = ROOT / ".agents/skills" / NAME


class MaintainerTests(unittest.TestCase):
    def test_frontmatter_and_ui_support_discovery(self):
        entry = SKILL / "SKILL.md"
        self.assertTrue(entry.is_file(), "Repository maintainer skill is missing")
        _, frontmatter, body = entry.read_text().split("---", 2)
        front = yaml.safe_load(frontmatter)
        self.assertEqual(NAME, front["name"])
        self.assertTrue(0 < len(front["description"]) <= 1024)
        self.assertLessEqual(len(body.split()), 500)
        ui = yaml.safe_load((SKILL / "agents/openai.yaml").read_text())
        self.assertTrue(25 <= len(ui["interface"]["short_description"]) <= 64)
        self.assertIn("$" + NAME, ui["interface"]["default_prompt"])
        self.assertTrue(ui.get("policy", {}).get("allow_implicit_invocation", True))

    def test_references_are_reachable_and_stay_in_the_skill(self):
        self.assertTrue(SKILL.is_dir(), "Repository maintainer skill is missing")
        references = set((SKILL / "references").glob("*.md"))
        self.assertTrue(references, "Maintainer procedures are missing")
        visited, pending = set(), [SKILL / "SKILL.md"]
        while pending:
            document = pending.pop()
            if document in visited:
                continue
            visited.add(document)
            content = document.read_text()
            self.assertEqual(0, sum(line.startswith("```") for line in content.splitlines()) % 2)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                parsed = urlsplit(target)
                if parsed.scheme in {"https", "http"}:
                    continue
                self.assertFalse(parsed.scheme or parsed.netloc, target)
                if not parsed.path:
                    continue
                linked = (document.parent / unquote(parsed.path)).resolve()
                self.assertTrue(linked.is_relative_to(SKILL.resolve()), target)
                self.assertTrue(linked.is_file(), target)
                if linked.suffix == ".md":
                    pending.append(linked)
        self.assertTrue({p.resolve() for p in references} <= {p.resolve() for p in visited})

    def test_agent_aliases_share_one_canonical_skill(self):
        for agent in [".codex", ".claude"]:
            with self.subTest(agent=agent):
                alias = ROOT / agent / "skills" / NAME
                self.assertTrue(alias.is_symlink(), f"Missing relative skill alias: {alias}")
                self.assertEqual(Path("../../.agents/skills") / NAME, alias.readlink())
                self.assertTrue((alias / "SKILL.md").is_file())
                self.assertEqual(SKILL.resolve(), alias.resolve())


if __name__ == "__main__":
    unittest.main()
