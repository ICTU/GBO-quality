#!/usr/bin/env python3
"""Kwaliteitskalender: maak issues voor periodieke taken en markeer te late issues (kwaliteitsplan §6).

Gebruik:
  kwaliteitskalender.py issues <kalender.yml> [--datum JJJJ-MM-DD] [--dry-run]
  kwaliteitskalender.py te-laat [--label kwaliteitskalender --label kwetsbaarheid ...] [--datum ...] [--dry-run]

`issues` maakt per taak één issue per periode, op elk moment binnen die periode; dubbele issues worden
voorkomen via de periode in de titel. Zo maakt het niet uit hoe vaak of wanneer de workflow draait.

`te-laat` zet het label `te-laat` op open issues waarvan de deadline (regel "**Uiterlijk:** JJJJ-MM-DD"
in de beschrijving) verstreken is. Quality-time kan het aantal te late issues meten.
"""
import argparse
import calendar
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

import gbo_gh

MAANDEN = {"maandelijks": 1, "kwartaal": 3, "halfjaarlijks": 6, "jaarlijks": 12}
LABEL = "kwaliteitskalender"
TE_LAAT = "te-laat"


def load(path: str) -> dict:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    for task in data.get("taken") or []:
        for field in ("id", "titel", "frequentie", "start"):
            if not task.get(field):
                raise ValueError(f"Taak {task.get('id', '?')}: veld '{field}' ontbreekt.")
        if task["frequentie"] not in MAANDEN:
            raise ValueError(f"Taak {task['id']}: onbekende frequentie '{task['frequentie']}'.")
    return data


def month_index(value) -> int:
    year, month = (int(x) for x in str(value).split("-")[:2])
    return year * 12 + (month - 1)


def period(task: dict, today: date) -> tuple[date, date] | None:
    """Begin en einde van de huidige periode van de taak, of None vóór de startmaand."""
    interval = MAANDEN[task["frequentie"]]
    start = month_index(task["start"])
    now = today.year * 12 + (today.month - 1)
    if now < start:
        return None
    first = start + ((now - start) // interval) * interval
    last = first + interval - 1
    begin = date(first // 12, first % 12 + 1, 1)
    end_year, end_month = last // 12, last % 12 + 1
    return begin, date(end_year, end_month, calendar.monthrange(end_year, end_month)[1])


def title(task: dict, begin: date) -> str:
    return f"{task['titel']} ({begin:%Y-%m})"


def deadline(task: dict, begin: date, end: date) -> date:
    return begin + timedelta(days=int(task["termijn"])) if task.get("termijn") else end


def body(task: dict, begin: date, end: date) -> str:
    lines = [f"**Uiterlijk:** {deadline(task, begin, end).isoformat()}", "",
             f"Periodieke taak uit de kwaliteitskalender (`{task['id']}`, {task['frequentie']}), "
             f"periode {begin.isoformat()} t/m {end.isoformat()}.", ""]
    if task.get("bron"):
        lines += [f"**Bron:** {task['bron']}", ""]
    if task.get("checklist"):
        lines += ["## Checklist", ""] + [f"- [ ] {item}" for item in task["checklist"]] + [""]
    if task.get("bewijs"):
        lines += ["## Bewijs", "", f"Voeg toe aan dit issue voordat je het sluit: {task['bewijs']}", ""]
    lines += ["<!-- kwaliteitskalender:" + task["id"] + " -->"]
    return "\n".join(lines)


def due(data: dict, today: date) -> list[tuple[dict, date, date]]:
    result = []
    for task in data.get("taken") or []:
        current = period(task, today)
        if current:
            result.append((task, *current))
    return result


def cmd_issues(args) -> int:
    data = load(args.kalender)
    today = date.fromisoformat(args.datum) if args.datum else date.today()
    todo = due(data, today)
    existing = set() if args.dry_run else {i["title"] for i in gbo_gh.issues(LABEL)}
    if not args.dry_run:
        gbo_gh.ensure_label(LABEL, "0e8a16", "Periodieke taak uit de kwaliteitskalender")
    for task, begin, end in todo:
        name = title(task, begin)
        if name in existing:
            print(f"Bestaat al: {name}")
            continue
        labels = [LABEL, *(task.get("labels") or [])]
        if args.dry_run:
            print(f"[dry-run] Zou aanmaken: {name} (labels: {', '.join(labels)})\n{body(task, begin, end)}\n")
            continue
        for label in labels[1:]:
            gbo_gh.ensure_label(label)
        assignees = [task["eigenaar"]] if task.get("eigenaar") else []
        print(f"Aangemaakt: {gbo_gh.create_issue(name, body(task, begin, end), labels, assignees)}")
    return 0


def cmd_te_laat(args) -> int:
    today = date.fromisoformat(args.datum) if args.datum else date.today()
    if not args.dry_run:
        gbo_gh.ensure_label(TE_LAAT, "b60205", "Deadline verstreken")
    for label in args.label or [LABEL]:
        for issue in gbo_gh.issues(label, state="open"):
            limit = gbo_gh.deadline(issue["body"])
            names = {lab["name"] for lab in issue["labels"]}
            if not limit or limit >= today or TE_LAAT in names:
                continue
            print(f"Te laat (deadline {limit}): #{issue['number']} {issue['title']}")
            if not args.dry_run:
                gbo_gh.gh("issue", "edit", str(issue["number"]), "--repo", gbo_gh.repo(), "--add-label", TE_LAAT)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_issues = sub.add_parser("issues")
    p_issues.add_argument("kalender")
    p_laat = sub.add_parser("te-laat")
    p_laat.add_argument("--label", action="append")
    for p in (p_issues, p_laat):
        p.add_argument("--datum")
        p.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return cmd_issues(args) if args.cmd == "issues" else cmd_te_laat(args)


if __name__ == "__main__":
    sys.exit(main())
