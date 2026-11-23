#!/usr/bin/env python3
"""Maak het testrapport van een release (kwaliteitsplan §4 en §8.8) uit bestanden die de pipeline al heeft.

Alle invoer is optioneel; wat ontbreekt, staat als aandachtspunt in het rapport.

  --tag              versie van de release (verplicht)
  --vorige-tag       vorige versie, voor de periode van het rapport
  --junit            map met JUnit-XML-bestanden (resultaten van de geautomatiseerde tests)
  --trivy            Trivy-resultaat in JSON
  --trivyignore      .trivyignore met geaccepteerde kwetsbaarheden
  --prs              prs.json van verzamel_releasegegevens.py
  --bugs             bugs.json van verzamel_releasegegevens.py
  --testgevallen     map met de logische testgevallen (bijv. docs/testgevallen)
  --bronmap          map waarin testbestanden naar LTC-ID's worden doorzocht (standaard .)
  --ltc-patroon      reguliere expressie voor een LTC-ID (standaard GBO-LTC-\\d+)
  --rollback         bestand met de rollbackinstructie (bijv. docs/rollback.md)
  --uit              uitvoerbestand (standaard testrapport.md)
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "vendor", ".venv", "venv", "dist", "build", "target", ".gbo-quality",
             ".bewijs"}
TEST_PATH = re.compile(r"(test|spec|conformance)", re.IGNORECASE)
ERNST = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]


# --- invoer lezen -------------------------------------------------------------------------------

def load_json(path: str | None):
    if not path or not Path(path).is_file():
        return None
    return json.loads(Path(path).read_text(encoding="utf-8") or "null")


def junit_results(folder: str | None) -> list[dict] | None:
    """Een rij per testgeval: suite, naam, status (geslaagd, gefaald, fout, overgeslagen), melding."""
    if not folder or not Path(folder).is_dir():
        return None
    results = []
    for file in sorted(Path(folder).rglob("*.xml")):
        try:
            root = ET.parse(file).getroot()
        except ET.ParseError:
            continue
        for case in root.iter("testcase"):
            status, message = "geslaagd", ""
            for tag, name in (("failure", "gefaald"), ("error", "fout"), ("skipped", "overgeslagen")):
                element = case.find(tag)
                if element is not None:
                    status = name
                    message = (element.get("message") or element.text or "").strip().splitlines()[:1]
                    message = message[0] if message else ""
                    break
            results.append({"suite": case.get("classname") or file.stem, "naam": case.get("name", ""),
                            "status": status, "melding": message})
    return results


def defined_ltcs(folder: str | None, pattern: re.Pattern) -> list[str] | None:
    if not folder or not Path(folder).is_dir():
        return None
    found = set()
    for file in Path(folder).rglob("*"):
        if file.is_file() and file.suffix.lower() in {".md", ".yml", ".yaml", ".txt", ".csv", ".feature"}:
            found.update(pattern.findall(file.read_text(encoding="utf-8", errors="ignore")))
    return sorted(found)


def ltcs_in_tests(root: str, pattern: re.Pattern, exclude: str | None) -> dict[str, list[str]]:
    """LTC-ID → testbestanden die het ID noemen. Alleen paden met test, spec of conformance erin."""
    base = Path(root)
    excluded = Path(exclude).resolve() if exclude else None
    found: dict[str, set[str]] = {}
    for file in base.rglob("*"):
        if not file.is_file() or any(part in SKIP_DIRS for part in file.relative_to(base).parts):
            continue
        if excluded and excluded in file.resolve().parents:
            continue
        rel = file.relative_to(base).as_posix()
        if not TEST_PATH.search(rel) or file.stat().st_size > 1_000_000:
            continue
        try:
            text = file.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for ltc in set(pattern.findall(text)):
            found.setdefault(ltc, set()).add(rel)
    return {ltc: sorted(files) for ltc, files in found.items()}


def trivy_findings(data) -> list[dict] | None:
    if data is None:
        return None
    findings = []
    for result in data.get("Results") or []:
        for vuln in result.get("Vulnerabilities") or []:
            findings.append({"id": vuln.get("VulnerabilityID", ""), "ernst": vuln.get("Severity", "UNKNOWN"),
                             "pakket": vuln.get("PkgName", ""), "versie": vuln.get("InstalledVersion", ""),
                             "opgelost_in": vuln.get("FixedVersion", ""), "titel": vuln.get("Title", ""),
                             "bron": result.get("Target", "")})
    return findings


def trivyignore_entries(path: str | None) -> list[dict] | None:
    if not path or not Path(path).is_file():
        return None
    entries, comment = [], []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("#"):
            comment.append(line.lstrip("# ").strip())
        elif line:
            parts = line.split()
            exp = next((p.split(":", 1)[1] for p in parts[1:] if p.startswith("exp:")), "")
            entries.append({"id": parts[0], "vervalt": exp, "toelichting": " ".join(comment)})
            comment = []
        else:
            comment = []
    return entries


# --- rapport ------------------------------------------------------------------------------------

def cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def build(args) -> str:
    pattern = re.compile(args.ltc_patroon)
    tests = junit_results(args.junit)
    defined = defined_ltcs(args.testgevallen, pattern)
    in_tests = ltcs_in_tests(args.bronmap, pattern, args.testgevallen)
    findings = trivy_findings(load_json(args.trivy))
    accepted = trivyignore_entries(args.trivyignore)
    prs = load_json(args.prs)
    bugs = load_json(args.bugs)
    rollback = Path(args.rollback) if args.rollback else None
    attention: list[str] = []

    out = [f"# Testrapport {args.tag}", ""]
    periode = f"sinds {args.vorige_tag}" if args.vorige_tag else "eerste release"
    out += [f"Automatisch gemaakt door de release-pipeline op "
            f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC ({periode}).", "",
            "Dit rapport hoort bij de bewijsbundel van de release (kwaliteitsplan §4, §6 en §8.8). "
            "Resultaten van tests buiten de pipeline, zoals pentests, worden vastgelegd in het kalender-issue van de pentest "
            "of in de informatie voor het vrijgaveadvies.", ""]

    body: list[str] = []

    # Geautomatiseerde tests
    body += ["## Geautomatiseerde tests", ""]
    if tests is None:
        body += ["Geen testresultaten (JUnit-XML) gevonden.", ""]
        attention.append("Geen testresultaten in de bewijsbundel: stel `test-command` en `junit-paden` in.")
    else:
        counts = Counter(t["status"] for t in tests)
        body += ["| Totaal | Geslaagd | Gefaald | Fout | Overgeslagen |", "|---|---|---|---|---|",
                 f"| {len(tests)} | {counts['geslaagd']} | {counts['gefaald']} | {counts['fout']} "
                 f"| {counts['overgeslagen']} |", ""]
        failed = [t for t in tests if t["status"] in ("gefaald", "fout")]
        if failed:
            attention.append(f"{len(failed)} geautomatiseerde test(s) niet geslaagd.")
            body += ["### Niet geslaagd", "", "| Suite | Test | Melding |", "|---|---|---|"]
            body += [f"| {cell(t['suite'])} | {cell(t['naam'])} | {cell(t['melding'])} |" for t in failed]
            body.append("")
        if not tests:
            attention.append("De JUnit-bestanden bevatten geen testgevallen.")

    # Traceerbaarheid
    body += ["## Traceerbaarheid logische testgevallen", ""]
    all_ltcs = sorted(set(defined or []) | set(in_tests))
    if not all_ltcs:
        body += [f"Geen logische testgevallen gevonden (patroon `{args.ltc_patroon}`).", ""]
        attention.append("Geen traceerbaarheid naar logische testgevallen aantoonbaar (M03).")
    else:
        body += ["| Logisch testgeval | Gedefinieerd | Testbestanden | Resultaat |", "|---|---|---|---|"]
        without_test = []
        for ltc in all_ltcs:
            files = in_tests.get(ltc, [])
            if defined is not None and ltc in defined and not files:
                without_test.append(ltc)
            result = "–"
            if tests:
                statuses = {t["status"] for t in tests if ltc in t["naam"] or ltc in t["suite"]}
                if statuses:
                    result = ("gefaald" if statuses & {"gefaald", "fout"} else
                              "geslaagd" if "geslaagd" in statuses else "overgeslagen")
            known = "ja" if defined and ltc in defined else ("nee" if defined is not None else "onbekend")
            body.append(f"| {ltc} | {known} | {cell(', '.join(files)) or '–'} | {result} |")
        body.append("")
        if defined is not None:
            covered = len(defined) - len(without_test)
            pct = round(100 * covered / len(defined)) if defined else 0
            body += [f"{covered} van {len(defined)} logische testgevallen hebben een geautomatiseerde test "
                     f"({pct}%; norm ≥ 80%).", ""]
            if defined and pct < 80:
                attention.append(f"Functionele testdekking {pct}% is lager dan de norm van 80%.")
        else:
            attention.append("Geen map met logische testgevallen opgegeven; dekking niet te bepalen.")
        body += ["Resultaat *–*: het ID komt niet voor in de namen in de testresultaten; zet het ID in de "
                 "testnaam om het resultaat per testgeval te zien.", ""]

    # Kwetsbaarheden
    body += ["## Kwetsbaarheden in dependencies", ""]
    if findings is None:
        body += ["Geen scanresultaat gevonden.", ""]
        attention.append("Geen kwetsbaarhedenscan in de bewijsbundel.")
    else:
        counts = Counter(f["ernst"] for f in findings)
        body += ["| " + " | ".join(e.capitalize() for e in ERNST) + " |", "|---|---|---|---|---|",
                 "| " + " | ".join(str(counts.get(e, 0)) for e in ERNST) + " |", ""]
        serious = [f for f in findings if f["ernst"] in ("CRITICAL", "HIGH")]
        if serious:
            attention.append(f"{len(serious)} kwetsbaarheid/kwetsbaarheden met ernst critical of high.")
            body += ["| ID | Ernst | Pakket | Versie | Opgelost in |", "|---|---|---|---|---|"]
            body += [f"| {cell(f['id'])} | {f['ernst']} | {cell(f['pakket'])} | {cell(f['versie'])} "
                     f"| {cell(f['opgelost_in']) or '–'} |" for f in serious]
            body.append("")
    if accepted:
        body += ["### Geaccepteerde kwetsbaarheden (.trivyignore)", "",
                 "| ID | Vervalt | Toelichting |", "|---|---|---|"]
        body += [f"| {cell(a['id'])} | {a['vervalt'] or '**geen vervaldatum**'} | {cell(a['toelichting'])} |"
                 for a in accepted]
        body.append("")
        if any(not a["vervalt"] for a in accepted):
            attention.append("Geaccepteerde kwetsbaarheid zonder vervaldatum in .trivyignore.")

    # Reviews
    body += ["## Wijzigingen en reviews", ""]
    if prs is None:
        body += ["Gegevens over pull requests niet beschikbaar (leesrechten op pull requests ontbreken).", ""]
        attention.append("Reviews niet aantoonbaar: geef de release-job `pull-requests: read`.")
    elif not prs:
        body += ["Geen gemergde pull requests in deze periode.", ""]
    else:
        unreviewed = [p for p in prs if not set(p["approvers"]) - {p["author"]}]
        body += [f"{len(prs)} pull requests gemerged, waarvan {len(prs) - len(unreviewed)} goedgekeurd door "
                 "een andere ontwikkelaar.", "",
                 "| PR | Titel | Auteur | Goedgekeurd door |", "|---|---|---|---|"]
        body += [f"| [#{p['number']}]({p['url']}) | {cell(p['title'])} | {p['author']} "
                 f"| {', '.join(p['approvers']) or '**geen**'} |" for p in prs]
        body.append("")
        if unreviewed:
            attention.append(f"{len(unreviewed)} pull request(s) zonder goedkeuring door een ander.")

    # Bugs
    body += ["## Openstaande bugs", ""]
    if bugs is None:
        body += ["Niet beschikbaar (leesrechten op issues ontbreken).", ""]
    elif not bugs:
        body += ["Geen openstaande issues met het label `bug`.", ""]
    else:
        body += ["| Issue | Titel | Labels |", "|---|---|---|"]
        body += [f"| [#{b['number']}]({b['url']}) | {cell(b['title'])} | {cell(', '.join(b['labels']))} |"
                 for b in bugs]
        body.append("")

    # Rollback
    body += ["## Rollbackinstructie", ""]
    if rollback and rollback.is_file():
        body += [rollback.read_text(encoding="utf-8").strip(), ""]
    else:
        body += ["Geen rollbackinstructie gevonden.", ""]
        attention.append("Rollbackinstructie ontbreekt (kwaliteitsplan §8.8): voeg `docs/rollback.md` toe.")

    out += ["## Samenvatting", ""]
    out += [f"- {a}" for a in attention] if attention else ["Geen aandachtspunten."]
    out += [""] + body
    return "\n".join(out).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--vorige-tag", default="")
    parser.add_argument("--junit")
    parser.add_argument("--trivy")
    parser.add_argument("--trivyignore")
    parser.add_argument("--prs")
    parser.add_argument("--bugs")
    parser.add_argument("--testgevallen")
    parser.add_argument("--bronmap", default=".")
    parser.add_argument("--ltc-patroon", default=r"GBO-LTC-\d+")
    parser.add_argument("--rollback")
    parser.add_argument("--uit", default="testrapport.md")
    args = parser.parse_args(argv)
    Path(args.uit).write_text(build(args), encoding="utf-8")
    print(f"Testrapport geschreven naar {args.uit}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
