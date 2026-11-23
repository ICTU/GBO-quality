#!/usr/bin/env python3
"""Maak issues voor kwetsbaarheden uit de nachtelijke scan en sluit ze als ze verdwenen zijn (kwaliteitsplan §8.4).

Gebruik: kwetsbaarheden.py <trivy.json> [<trivy.json> ...] [--ernst CRITICAL,HIGH] [--termijn 7]
                           [--trivyignore .trivyignore] [--dry-run]

- Per kwetsbaarheid (ID + pakket) met de opgegeven ernst één issue met het label `kwetsbaarheid` en een
  deadline. De standaardtermijn van 7 dagen volgt uit BIO2 8.08.01 (hoge kans op misbruik én hoge
  schade); de risicoafweging in het issue kan een andere termijn vastleggen.
- Komt een kwetsbaarheid van een gesloten issue terug (bijvoorbeeld omdat de uitzondering in
  .trivyignore is verlopen), dan wordt het issue heropend.
- Is de kwetsbaarheid van een open issue niet meer gevonden, dan wordt het issue gesloten met een notitie.
- Regels in .trivyignore zonder vervaldatum (exp:JJJJ-MM-DD) geven een waarschuwing.
"""
import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import gbo_gh

LABEL = "kwetsbaarheid"
MARKER = re.compile(r"<!-- kwetsbaarheid:(?P<key>[^ ]+) -->")


def findings(paths: list[str], severities: set[str]) -> dict[str, dict]:
    found: dict[str, dict] = {}
    for path in paths:
        data = json.loads(Path(path).read_text(encoding="utf-8") or "{}")
        for result in data.get("Results") or []:
            for vuln in result.get("Vulnerabilities") or []:
                if vuln.get("Severity") not in severities:
                    continue
                key = f"{vuln['VulnerabilityID']}@{vuln.get('PkgName', '')}"
                entry = found.setdefault(key, {
                    "id": vuln["VulnerabilityID"], "pakket": vuln.get("PkgName", ""),
                    "ernst": vuln.get("Severity", ""), "titel": vuln.get("Title", ""),
                    "url": vuln.get("PrimaryURL", ""), "opgelost_in": vuln.get("FixedVersion", ""),
                    "versies": set(), "bronnen": set()})
                entry["versies"].add(vuln.get("InstalledVersion", ""))
                entry["bronnen"].add(result.get("Target", ""))
    return found


def missing_expiry(path: str | None) -> list[str]:
    if not path or not Path(path).is_file():
        return []
    entries = [line.split() for line in Path(path).read_text(encoding="utf-8").splitlines()
               if line.strip() and not line.strip().startswith("#")]
    return [parts[0] for parts in entries if not any(p.startswith("exp:") for p in parts[1:])]


def issue_title(f: dict) -> str:
    return f"Kwetsbaarheid {f['id']} ({f['ernst'].lower()}) in {f['pakket']}"


def issue_body(key: str, f: dict, deadline: date) -> str:
    fixed = f["opgelost_in"] or "nog geen versie met een oplossing"
    return "\n".join([
        f"**Uiterlijk:** {deadline.isoformat()}", "",
        f"De nachtelijke scan vond **{f['id']}** ({f['ernst']}) in `{f['pakket']}` "
        f"(versie {', '.join(sorted(f['versies']))}). Opgelost in: {fixed}.", "",
        f"- Titel: {f['titel'] or '–'}",
        f"- Details: {f['url'] or '–'}",
        f"- Gevonden in: {', '.join(sorted(f['bronnen']))}", "",
        "## Afhandeling (kwaliteitsplan §8.4; bron: BIO2 v1.3, 8.08.01-8.08.03)", "",
        "- [ ] Risicoafweging vastgelegd in dit issue: kans op misbruik en verwachte schade",
        "- [ ] Beide hoog: patchrelease of mitigatieadvies aan beheerders en bronhouders vóór de deadline",
        "- [ ] Anders: termijn vastgelegd (pas de regel *Uiterlijk* hierboven aan) of uitzondering in "
        "`.trivyignore` met reden, issuenummer en `exp:JJJJ-MM-DD`",
        "- [ ] Uitgebrachte versies die geraakt zijn benoemd", "",
        "Dit issue wordt automatisch gesloten zodra de scan de kwetsbaarheid niet meer vindt.", "",
        f"<!-- kwetsbaarheid:{key} -->"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("scans", nargs="+")
    parser.add_argument("--ernst", default="CRITICAL,HIGH")
    parser.add_argument("--termijn", type=int, default=7)
    parser.add_argument("--trivyignore", default=".trivyignore")
    parser.add_argument("--datum")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    today = date.fromisoformat(args.datum) if args.datum else date.today()
    for cve in missing_expiry(args.trivyignore):
        print(f"::warning::{cve} in .trivyignore heeft geen vervaldatum (exp:JJJJ-MM-DD).")

    current = findings(args.scans, {s.strip().upper() for s in args.ernst.split(",")})
    print(f"{len(current)} kwetsbaarheid/kwetsbaarheden met ernst {args.ernst} gevonden.")
    if args.dry_run:
        for key, f in current.items():
            print(f"[dry-run] {issue_title(f)}\n{issue_body(key, f, today + timedelta(days=args.termijn))}\n")
        return 0

    gbo_gh.ensure_label(LABEL, "d93f0b", "Kwetsbaarheid uit de nachtelijke scan")
    gbo_gh.ensure_label("security", "b60205", "Beveiliging")
    known: dict[str, dict] = {}
    for issue in gbo_gh.issues(LABEL):
        match = MARKER.search(issue["body"] or "")
        if match and (match.group("key") not in known or issue["state"] == "OPEN"):
            known[match.group("key")] = issue

    for key, f in current.items():
        issue = known.get(key)
        if issue is None:
            url = gbo_gh.create_issue(issue_title(f), issue_body(key, f, today + timedelta(days=args.termijn)),
                                      [LABEL, "security"])
            print(f"Aangemaakt: {url}")
        elif issue["state"] != "OPEN":
            gbo_gh.gh("issue", "reopen", str(issue["number"]), "--repo", gbo_gh.repo(), "--comment",
                      f"Opnieuw gevonden in de scan van {today.isoformat()}; issue heropend.")
            print(f"Heropend: #{issue['number']} {issue['title']}")

    for key, issue in known.items():
        if issue["state"] == "OPEN" and key not in current:
            gbo_gh.gh("issue", "close", str(issue["number"]), "--repo", gbo_gh.repo(), "--comment",
                      f"Niet meer gevonden in de scan van {today.isoformat()}; automatisch gesloten.")
            print(f"Gesloten: #{issue['number']} {issue['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
