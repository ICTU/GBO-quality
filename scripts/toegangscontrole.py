#!/usr/bin/env python3
"""Controleer toegang tot de repository: MFA, beheerders en bescherming van main (kwaliteitsplan §8.5).

Gebruik: toegangscontrole.py <kalender.yml> [--rapport toegang.md] [--dry-run]

Controleert:
- of de GitHub-organisatie MFA verplicht stelt en welke leden geen MFA hebben (bron: BIO2 v1.3, 5.17.01);
- of alleen de beheerders uit de kalender (`beheerders:`) beheerrechten hebben;
- of de standaardbranch beschermd is: pull request met review, verplichte checks, geen force-push.

Het rapport komt in de samenvatting van de workflow-run (bewijs van bestaan en werking). Bij een
afwijking komt er één issue met het label `toegangscontrole`, dat automatisch sluit als alles weer klopt.
Voor de organisatiegegevens is een token met leesrecht op de organisatie nodig (GBO_AUDIT_TOKEN); zonder
dat token staan die punten als "niet te controleren" in het rapport, zonder issue.
"""
import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

import gbo_gh

LABEL = "toegangscontrole"
TITLE = "Afwijking in de toegangscontrole"


def safe(call, *args, **kwargs):
    try:
        return call(*args, **kwargs), None
    except RuntimeError as error:
        return None, str(error).split(" mislukt: ", 1)[-1].splitlines()[0][:200]


def check_org(org: str) -> tuple[list[str], list[str]]:
    lines, problems = [], []
    info, error = safe(gbo_gh.api, f"orgs/{org}")
    mfa = (info or {}).get("two_factor_requirement_enabled")
    if mfa is None:
        lines.append(f"- MFA verplicht in organisatie `{org}`: niet te controleren ({error or 'geen leesrecht'})")
    elif mfa:
        lines.append(f"- MFA verplicht in organisatie `{org}`: ja")
    else:
        lines.append(f"- MFA verplicht in organisatie `{org}`: **nee**")
        problems.append(f"De organisatie {org} stelt MFA niet verplicht.")
    members, error = safe(gbo_gh.api, f"orgs/{org}/members?filter=2fa_disabled", paginate=True)
    if members is None:
        lines.append(f"- Leden zonder MFA: niet te controleren ({error})")
    elif members:
        names = ", ".join(sorted(m["login"] for m in members))
        lines.append(f"- Leden zonder MFA: **{names}**")
        problems.append(f"Leden zonder MFA: {names}.")
    else:
        lines.append("- Leden zonder MFA: geen")
    return lines, problems


def check_admins(allowed: set[str]) -> tuple[list[str], list[str]]:
    collaborators, error = safe(gbo_gh.api, f"repos/{gbo_gh.repo()}/collaborators?affiliation=all&per_page=100",
                                paginate=True)
    if collaborators is None:
        return [f"- Beheerders: niet te controleren ({error})"], []
    admins = sorted(c["login"] for c in collaborators if (c.get("permissions") or {}).get("admin"))
    writers = sorted(c["login"] for c in collaborators
                     if (c.get("permissions") or {}).get("push") and c["login"] not in admins)
    lines = [f"- Beheerders: {', '.join(admins) or 'geen'}",
             f"- Schrijfrechten: {', '.join(writers) or 'geen'}"]
    extra = [a for a in admins if a not in allowed]
    if extra:
        lines.append(f"- Beheerders die niet in de kalender staan: **{', '.join(extra)}**")
        return lines, [f"Beheerrechten voor gebruikers die niet als beheerder zijn benoemd: {', '.join(extra)}."]
    return lines, []


def check_branch() -> tuple[list[str], list[str]]:
    info, error = safe(gbo_gh.api, f"repos/{gbo_gh.repo()}")
    if info is None:
        return [f"- Bescherming standaardbranch: niet te controleren ({error})"], []
    branch = info["default_branch"]
    rules, error = safe(gbo_gh.api, f"repos/{gbo_gh.repo()}/rules/branches/{branch}", paginate=True)
    rules = rules or []
    types = {r["type"]: r.get("parameters") or {} for r in rules}
    lines, problems = [f"- Standaardbranch: `{branch}`"], []
    if not rules:
        plain, _ = safe(gbo_gh.api, f"repos/{gbo_gh.repo()}/branches/{branch}")
        if plain and plain.get("protected"):
            lines.append("- Beschermd met klassieke branch protection; details alleen zichtbaar voor beheerders. "
                         "Gebruik bij voorkeur een ruleset, dan controleert deze check de details.")
            return lines, problems
        lines.append("- **Geen bescherming gevonden**")
        return lines, [f"De standaardbranch {branch} is niet beschermd."]
    review = types.get("pull_request")
    approvals = (review or {}).get("required_approving_review_count", 0)
    checks = [c.get("context") for c in (types.get("required_status_checks") or {})
              .get("required_status_checks", [])]
    expectations = [
        ("Pull request verplicht", review is not None),
        (f"Minimaal 1 goedkeuring (nu {approvals})", approvals >= 1),
        ("Review door code owners", bool((review or {}).get("require_code_owner_review"))),
        ("Goedkeuring vervalt bij nieuwe commits", bool((review or {}).get("dismiss_stale_reviews_on_push"))),
        (f"Verplichte checks ({', '.join(checks) or 'geen'})", bool(checks)),
        ("Force-push geblokkeerd", "non_fast_forward" in types),
        ("Verwijderen geblokkeerd", "deletion" in types),
    ]
    for text, ok in expectations:
        lines.append(f"- {text}: {'ja' if ok else '**nee**'}")
        if not ok:
            problems.append(f"Bescherming van {branch}: {text.lower()} ontbreekt.")
    return lines, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("kalender")
    parser.add_argument("--rapport", default="toegangscontrole.md")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    config = yaml.safe_load(Path(args.kalender).read_text(encoding="utf-8")) or {}
    allowed = {str(name) for name in config.get("beheerders") or []}
    org = gbo_gh.repo().split("/")[0]

    report = [f"# Toegangscontrole {gbo_gh.repo()} ({date.today().isoformat()})", ""]
    problems: list[str] = []
    for heading, (lines, found) in (("Organisatie", check_org(org)), ("Repository", check_admins(allowed)),
                                     ("Bescherming", check_branch())):
        report += [f"## {heading}", "", *lines, ""]
        problems += found
    report += ["## Afwijkingen", ""] + ([f"- {p}" for p in problems] or ["Geen."])
    text = "\n".join(report) + "\n"
    Path(args.rapport).write_text(text, encoding="utf-8")
    print(text)

    if args.dry_run:
        return 0
    gbo_gh.ensure_label(LABEL, "b60205", "Afwijking in de automatische toegangscontrole")
    gbo_gh.ensure_label("security", "b60205", "Beveiliging")
    open_issues = [i for i in gbo_gh.issues(LABEL, state="open") if i["title"] == TITLE]
    if problems and not open_issues:
        print("Aangemaakt:", gbo_gh.create_issue(TITLE, text, [LABEL, "security"]))
    elif problems:
        gbo_gh.gh("issue", "edit", str(open_issues[0]["number"]), "--repo", gbo_gh.repo(), "--body-file", "-",
                  input_text=text)
        print(f"Bijgewerkt: #{open_issues[0]['number']}")
    for issue in open_issues if not problems else []:
        gbo_gh.gh("issue", "close", str(issue["number"]), "--repo", gbo_gh.repo(), "--comment",
                  "De toegangscontrole vindt geen afwijkingen meer; automatisch gesloten.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
