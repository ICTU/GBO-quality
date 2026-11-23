import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import gbo_gh  # noqa: E402
import kwaliteitskalender  # noqa: E402
import kwetsbaarheden  # noqa: E402
import testrapport  # noqa: E402
import toegangscontrole  # noqa: E402

JUNIT = """<?xml version="1.0"?>
<testsuites>
  <testsuite name="api">
    <testcase classname="api.Autorisatie" name="test_weigert_zonder_contract_GBO-LTC-001"/>
    <testcase classname="api.Autorisatie" name="test_logregel_GBO-LTC-002">
      <failure message="verwacht 'geweigerd'">details</failure>
    </testcase>
    <testcase classname="api.Overig" name="test_overgeslagen"><skipped/></testcase>
  </testsuite>
</testsuites>
"""

TRIVY = {"Results": [{"Target": "go.mod", "Vulnerabilities": [
    {"VulnerabilityID": "CVE-2026-0001", "PkgName": "golang.org/x/net", "InstalledVersion": "0.1.0",
     "FixedVersion": "0.2.0", "Severity": "HIGH", "Title": "Iets ergs"},
    {"VulnerabilityID": "CVE-2026-0002", "PkgName": "lib", "InstalledVersion": "1.0", "Severity": "LOW"},
]}]}


class TestrapportTest(unittest.TestCase):
    def maak(self, folder: Path, **extra) -> str:
        (folder / "junit").mkdir()
        (folder / "junit/junit.xml").write_text(JUNIT, encoding="utf-8")
        (folder / "trivy.json").write_text(json.dumps(TRIVY), encoding="utf-8")
        (folder / "docs/testgevallen").mkdir(parents=True)
        (folder / "docs/testgevallen/autorisatie.md").write_text(
            "## GBO-LTC-001\n## GBO-LTC-002\n## GBO-LTC-003\n", encoding="utf-8")
        (folder / "tests").mkdir()
        (folder / "tests/test_api.py").write_text("# LTC: GBO-LTC-001\n# LTC: GBO-LTC-002\n", encoding="utf-8")
        (folder / "README.md").write_text("GBO-LTC-003 wordt hier alleen genoemd\n", encoding="utf-8")
        (folder / ".trivyignore").write_text("# reden\nCVE-2026-9999\n", encoding="utf-8")
        (folder / "prs.json").write_text(json.dumps([
            {"number": 1, "title": "feat: a", "url": "u", "author": "anna", "approvers": ["bert"]},
            {"number": 2, "title": "fix: b", "url": "u", "author": "anna", "approvers": ["anna"]},
        ]), encoding="utf-8")
        args = ["--tag", "v1.0.0", "--junit", str(folder / "junit"), "--trivy", str(folder / "trivy.json"),
                "--trivyignore", str(folder / ".trivyignore"), "--prs", str(folder / "prs.json"),
                "--testgevallen", str(folder / "docs/testgevallen"), "--bronmap", str(folder),
                "--uit", str(folder / "rapport.md"), *extra.get("args", [])]
        with contextlib.redirect_stdout(io.StringIO()):
            testrapport.main(args)
        return (folder / "rapport.md").read_text(encoding="utf-8")

    def test_rapport(self):
        with tempfile.TemporaryDirectory() as tmp:
            rapport = self.maak(Path(tmp))
        self.assertIn("| 3 | 1 | 1 | 0 | 1 |", rapport)
        self.assertIn("| GBO-LTC-001 | ja | tests/test_api.py | geslaagd |", rapport)
        self.assertIn("| GBO-LTC-002 | ja | tests/test_api.py | gefaald |", rapport)
        self.assertIn("| GBO-LTC-003 | ja | – | – |", rapport)  # README telt niet als test
        self.assertIn("2 van 3 logische testgevallen", rapport)
        self.assertIn("lager dan de norm van 80%", rapport)
        self.assertIn("CVE-2026-0001", rapport)
        self.assertIn("**geen vervaldatum**", rapport)
        self.assertIn("1 pull request(s) zonder goedkeuring door een ander", rapport)
        self.assertIn("Rollbackinstructie ontbreekt", rapport)
        self.assertIn("Openstaande bugs", rapport)

    def test_rollback_opgenomen(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "rollback.md").write_text("Zet image-tag terug.", encoding="utf-8")
            rapport = self.maak(Path(tmp), args=["--rollback", str(Path(tmp) / "rollback.md")])
        self.assertIn("Zet image-tag terug.", rapport)
        self.assertNotIn("Rollbackinstructie ontbreekt", rapport)

    def test_zonder_invoer(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "r.md"
            with contextlib.redirect_stdout(io.StringIO()):
                testrapport.main(["--tag", "v0.1.0", "--bronmap", tmp, "--uit", str(out)])
            rapport = out.read_text(encoding="utf-8")
        self.assertIn("Geen testresultaten in de bewijsbundel", rapport)
        self.assertIn("Geen kwetsbaarhedenscan", rapport)
        self.assertIn("Reviews niet aantoonbaar", rapport)


class KalenderTest(unittest.TestCase):
    TAAK = {"id": "pentest", "titel": "Pentest", "frequentie": "halfjaarlijks", "start": "2027-01",
            "termijn": 30, "bron": "M26", "checklist": ["a"], "bewijs": "rapport"}

    def test_periode(self):
        self.assertIsNone(kwaliteitskalender.period(self.TAAK, date(2026, 12, 31)))
        self.assertEqual(kwaliteitskalender.period(self.TAAK, date(2027, 3, 15)),
                         (date(2027, 1, 1), date(2027, 6, 30)))
        self.assertEqual(kwaliteitskalender.period(self.TAAK, date(2027, 7, 1)),
                         (date(2027, 7, 1), date(2027, 12, 31)))
        jaar = {**self.TAAK, "frequentie": "jaarlijks", "start": "2027-04"}
        self.assertEqual(kwaliteitskalender.period(jaar, date(2028, 2, 1)), (date(2027, 4, 1), date(2028, 3, 31)))

    def test_titel_en_deadline(self):
        begin, end = kwaliteitskalender.period(self.TAAK, date(2027, 2, 1))
        self.assertEqual(kwaliteitskalender.title(self.TAAK, begin), "Pentest (2027-01)")
        body = kwaliteitskalender.body(self.TAAK, begin, end)
        self.assertEqual(gbo_gh.deadline(body), date(2027, 1, 31))
        self.assertIn("- [ ] a", body)
        zonder_termijn = {k: v for k, v in self.TAAK.items() if k != "termijn"}
        self.assertEqual(gbo_gh.deadline(kwaliteitskalender.body(zonder_termijn, begin, end)), date(2027, 6, 30))

    def test_template_is_geldig(self):
        data = kwaliteitskalender.load(str(ROOT / "templates/.github/kwaliteitskalender.yml"))
        self.assertGreaterEqual(len(data["taken"]), 5)
        self.assertEqual(len({t["id"] for t in data["taken"]}), len(data["taken"]))
        self.assertTrue(kwaliteitskalender.due(data, date(2028, 1, 1)))

    def test_ongeldige_frequentie(self):
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            f.write("taken:\n  - {id: x, titel: X, frequentie: wekelijks, start: 2027-01}\n")
        with self.assertRaises(ValueError):
            kwaliteitskalender.load(f.name)

    def test_issues_zonder_dubbelen(self):
        bestaand = [{"title": "Pentest (2027-01)"}]
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False) as f:
            f.write("taken:\n  - {id: pentest, titel: Pentest, frequentie: halfjaarlijks, start: 2027-01}\n"
                    "  - {id: training, titel: Training, frequentie: jaarlijks, start: 2027-01}\n")
        with mock.patch.object(gbo_gh, "issues", return_value=bestaand), \
                mock.patch.object(gbo_gh, "ensure_label"), \
                mock.patch.object(gbo_gh, "create_issue", return_value="url") as create, \
                contextlib.redirect_stdout(io.StringIO()):
            kwaliteitskalender.main(["issues", f.name, "--datum", "2027-02-01"])
        self.assertEqual([c.args[0] for c in create.call_args_list], ["Training (2027-01)"])

    def test_te_laat(self):
        open_issues = [
            {"number": 1, "title": "a", "body": "**Uiterlijk:** 2027-01-31", "labels": []},
            {"number": 2, "title": "b", "body": "**Uiterlijk:** 2027-03-01", "labels": []},
            {"number": 3, "title": "c", "body": "**Uiterlijk:** 2027-01-01", "labels": [{"name": "te-laat"}]},
        ]
        with mock.patch.object(gbo_gh, "issues", return_value=open_issues), \
                mock.patch.object(gbo_gh, "ensure_label"), \
                mock.patch.object(gbo_gh, "repo", return_value="o/r"), \
                mock.patch.object(gbo_gh, "gh") as gh, contextlib.redirect_stdout(io.StringIO()):
            kwaliteitskalender.main(["te-laat", "--datum", "2027-02-01"])
        self.assertEqual([c.args[2] for c in gh.call_args_list], ["1"])


class KwetsbaarhedenTest(unittest.TestCase):
    def scan(self, folder: Path) -> str:
        path = folder / "trivy.json"
        path.write_text(json.dumps(TRIVY), encoding="utf-8")
        return str(path)

    def test_bevindingen_en_vervaldatum(self):
        with tempfile.TemporaryDirectory() as tmp:
            found = kwetsbaarheden.findings([self.scan(Path(tmp))], {"CRITICAL", "HIGH"})
            ignore = Path(tmp) / ".trivyignore"
            ignore.write_text("# x\nCVE-1 exp:2027-01-01\nCVE-2\n", encoding="utf-8")
            self.assertEqual(kwetsbaarheden.missing_expiry(str(ignore)), ["CVE-2"])
        self.assertEqual(list(found), ["CVE-2026-0001@golang.org/x/net"])
        body = kwetsbaarheden.issue_body("k", found["CVE-2026-0001@golang.org/x/net"], date(2027, 1, 8))
        self.assertEqual(gbo_gh.deadline(body), date(2027, 1, 8))

    def test_aanmaken_heropenen_sluiten(self):
        bestaand = [
            {"number": 5, "title": "x", "state": "CLOSED", "labels": [],
             "body": "<!-- kwetsbaarheid:CVE-2026-0001@golang.org/x/net -->"},
            {"number": 6, "title": "oud", "state": "OPEN", "labels": [],
             "body": "<!-- kwetsbaarheid:CVE-2025-1@weg -->"},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            scan = self.scan(Path(tmp))
            with mock.patch.object(gbo_gh, "issues", return_value=bestaand), \
                    mock.patch.object(gbo_gh, "ensure_label"), \
                    mock.patch.object(gbo_gh, "repo", return_value="o/r"), \
                    mock.patch.object(gbo_gh, "create_issue") as create, \
                    mock.patch.object(gbo_gh, "gh") as gh, contextlib.redirect_stdout(io.StringIO()):
                kwetsbaarheden.main([scan, "--trivyignore", str(Path(tmp) / "geen"), "--datum", "2027-01-01"])
        create.assert_not_called()
        acties = [(c.args[1], c.args[2]) for c in gh.call_args_list]
        self.assertEqual(acties, [("reopen", "5"), ("close", "6")])


class ToegangTest(unittest.TestCase):
    def api(self, rules):
        def fake(path, paginate=False):
            if path == "repos/o/r":
                return {"default_branch": "main"}
            if path.startswith("repos/o/r/rules/branches/"):
                return rules
            if path == "repos/o/r/branches/main":
                return {"protected": False}
            raise RuntimeError("geen toegang")
        return fake

    def test_goed_beschermd(self):
        rules = [{"type": "pull_request", "parameters": {"required_approving_review_count": 1,
                                                         "require_code_owner_review": True,
                                                         "dismiss_stale_reviews_on_push": True}},
                 {"type": "required_status_checks",
                  "parameters": {"required_status_checks": [{"context": "quality / ci"}]}},
                 {"type": "non_fast_forward"}, {"type": "deletion"}]
        with mock.patch.object(gbo_gh, "api", side_effect=self.api(rules)), \
                mock.patch.object(gbo_gh, "repo", return_value="o/r"):
            _, problems = toegangscontrole.check_branch()
        self.assertEqual(problems, [])

    def test_onbeschermd(self):
        with mock.patch.object(gbo_gh, "api", side_effect=self.api([])), \
                mock.patch.object(gbo_gh, "repo", return_value="o/r"):
            _, problems = toegangscontrole.check_branch()
        self.assertEqual(problems, ["De standaardbranch main is niet beschermd."])

    def test_zonder_audittoken_geen_afwijking(self):
        with mock.patch.object(gbo_gh, "api", side_effect=RuntimeError("403")), \
                mock.patch.object(gbo_gh, "repo", return_value="o/r"):
            lines, problems = toegangscontrole.check_org("o")
            admin_lines, admin_problems = toegangscontrole.check_admins({"anna"})
        self.assertEqual(problems + admin_problems, [])
        self.assertIn("niet te controleren", lines[0])
        self.assertIn("niet te controleren", admin_lines[0])

    def test_onbekende_beheerder(self):
        collaborators = [{"login": "anna", "permissions": {"admin": True, "push": True}},
                         {"login": "eve", "permissions": {"admin": True, "push": True}},
                         {"login": "bert", "permissions": {"admin": False, "push": True}}]
        with mock.patch.object(gbo_gh, "api", return_value=collaborators), \
                mock.patch.object(gbo_gh, "repo", return_value="o/r"):
            lines, problems = toegangscontrole.check_admins({"anna"})
        self.assertIn("eve", problems[0])
        self.assertIn("- Schrijfrechten: bert", lines)


if __name__ == "__main__":
    unittest.main()
