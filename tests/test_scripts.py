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


class VoorwaardelijkeDodTest(unittest.TestCase):
    RULES = "koppelvlak: api/** **/*.graphql\nui: frontend/**  # commentaar\nrisico: .github/deploy/**"
    BODY = ("<!-- dod:start -->\n- [x] altijd\n- [ ] conformance <!-- dod:koppelvlak -->\n"
            "- [ ] a11y <!-- dod:ui -->\n<!-- dod:end -->")

    def env(self, changed, body=None, rules=None):
        env = {"PR_BODY": body or self.BODY, "DOD_RULES": self.RULES if rules is None else rules}
        if changed is not None:
            env["CHANGED_FILES"] = "\n".join(changed)
        return env

    def test_paden_niet_geraakt(self):
        self.assertEqual(run("check_dod.py", self.env(["src/main.go", "README.md"])), 0)

    def test_koppelvlak_geraakt(self):
        self.assertEqual(run("check_dod.py", self.env(["schema/bron.graphql"])), 1)

    def test_koppelvlak_geraakt_en_afgevinkt(self):
        body = self.BODY.replace("- [ ] conformance", "- [x] conformance")
        self.assertEqual(run("check_dod.py", self.env(["api/v1/x.go"], body)), 0)

    def test_geraakt_met_nvt(self):
        body = self.BODY.replace("conformance", "conformance n.v.t.: alleen commentaar")
        self.assertEqual(run("check_dod.py", self.env(["api/x.go"], body)), 0)

    def test_zonder_gewijzigde_bestanden_geldt_alles(self):
        self.assertEqual(run("check_dod.py", self.env(None)), 1)

    def test_zonder_regels_geldt_alles(self):
        self.assertEqual(run("check_dod.py", self.env(["src/main.go"], rules="")), 1)

    def test_item_zonder_sleutel_blijft_verplicht(self):
        body = self.BODY.replace("- [x] altijd", "- [ ] altijd")
        self.assertEqual(run("check_dod.py", self.env(["src/main.go"], body)), 1)

    def test_patronen(self):
        sys.path.insert(0, str(SCRIPTS))
        import check_dod
        rules = check_dod.parse_rules(self.RULES)
        self.assertTrue(check_dod.applies("koppelvlak", rules, ["a/b/c.graphql"]))
        self.assertTrue(check_dod.applies("koppelvlak", rules, ["api/x/y.go"]))
        self.assertFalse(check_dod.applies("koppelvlak", rules, ["apis/x.go"]))
        self.assertFalse(check_dod.applies("ui", rules, ["src/frontend/x.tsx"]))
        self.assertTrue(check_dod.applies("risico", rules, [".github/deploy/a.yml"]))
        self.assertFalse(check_dod.applies("risico", rules, ["github/deploy/a.yml"]))

    def test_template_met_regels_uit_ci_template(self):
        ci = (TEMPLATE.parent / "workflows/ci.yml").read_text(encoding="utf-8")
        rules = ci.split("dod-regels: |", 1)[1].split("\n\n", 1)[0]
        body = TEMPLATE.read_text(encoding="utf-8")
        for item in ["Tests verwijzen", "Documentatie is", "Architectuurbeslissing", "Geen secrets"]:
            body = body.replace(f"- [ ] {item}", f"- [x] {item}")
        self.assertEqual(run("check_dod.py", self.env(["cmd/main.go"], body, rules)), 0)
        self.assertEqual(run("check_dod.py", self.env(["api/schema.graphql"], body, rules)), 1)


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
