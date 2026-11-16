import os
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
TEMPLATE = Path(__file__).resolve().parent.parent / "templates/.github/pull_request_template.md"


def run(script, env):
    full_env = {**os.environ, **env}
    return subprocess.run([sys.executable, str(SCRIPTS / script)], env=full_env,
                          capture_output=True, text=True).returncode


class CheckDodTest(unittest.TestCase):
    def body(self, items):
        return "<!-- dod:start -->\n" + "\n".join(items) + "\n<!-- dod:end -->"

    def test_alles_afgevinkt(self):
        self.assertEqual(run("check_dod.py", {"PR_BODY": self.body(["- [x] a", "- [X] b"])}), 0)

    def test_nvt_met_reden(self):
        self.assertEqual(run("check_dod.py", {"PR_BODY": self.body(["- [x] a", "- [ ] b n.v.t.: geen UI"])}), 0)

    def test_nvt_zonder_reden(self):
        self.assertEqual(run("check_dod.py", {"PR_BODY": self.body(["- [ ] b n.v.t."])}), 1)

    def test_open_item(self):
        self.assertEqual(run("check_dod.py", {"PR_BODY": self.body(["- [x] a", "- [ ] b"])}), 1)

    def test_geen_sectie(self):
        self.assertEqual(run("check_dod.py", {"PR_BODY": "geen template"}), 1)

    def test_leeg_template_faalt(self):
        self.assertEqual(run("check_dod.py", {"PR_BODY": TEMPLATE.read_text(encoding="utf-8")}), 1)


class CheckTraceabilityTest(unittest.TestCase):
    def test_jira_sleutel(self):
        self.assertEqual(run("check_traceability.py", {"PR_TITLE": "feat: x (GBO-12)", "PR_BODY": ""}), 0)

    def test_github_issue(self):
        self.assertEqual(run("check_traceability.py", {"PR_TITLE": "feat", "PR_BODY": "Closes #4"}), 0)

    def test_geen_verwijzing(self):
        self.assertEqual(run("check_traceability.py", {"PR_TITLE": "feat: x", "PR_BODY": "tekst"}), 1)

    def test_eigen_patroon(self):
        env = {"PR_TITLE": "feat: x (STORY-7)", "PR_BODY": "", "TRACE_PATTERN": r"\bGBO-\d+\b"}
        self.assertEqual(run("check_traceability.py", env), 1)


if __name__ == "__main__":
    unittest.main()
