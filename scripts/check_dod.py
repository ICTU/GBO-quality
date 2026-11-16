#!/usr/bin/env python3
"""Controleer of alle Definition of Done-items in een PR-beschrijving zijn afgehandeld.

Leest de PR-beschrijving uit de omgevingsvariabele PR_BODY (of uit een bestand als eerste argument).
Alleen checkboxes tussen de markeringen <!-- dod:start --> en <!-- dod:end --> tellen mee.
Een item is afgehandeld als het is afgevinkt ([x]) of de tekst "n.v.t." bevat met een toelichting.

Exitcode 0: alles afgehandeld. Exitcode 1: open items of geen DoD-sectie gevonden.
"""
import os
import re
import sys

START = "<!-- dod:start -->"
END = "<!-- dod:end -->"
CHECKBOX = re.compile(r"^\s*[-*]\s*\[(?P<state>[ xX])\]\s*(?P<text>.+)$")
NVT = re.compile(r"\bn\.?v\.?t\.?\b\s*[:\-–]?\s*(?P<reason>.*)", re.IGNORECASE)


def read_body() -> str:
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as handle:
            return handle.read()
    return os.environ.get("PR_BODY", "")


def check(body: str) -> list[str]:
    if START not in body or END not in body:
        return ["De PR-beschrijving bevat geen Definition of Done-sectie. Gebruik het PR-template."]
    section = body.split(START, 1)[1].split(END, 1)[0]
    problems = []
    items = 0
    for line in section.splitlines():
        match = CHECKBOX.match(line)
        if not match:
            continue
        items += 1
        text = match.group("text").strip()
        if match.group("state").lower() == "x":
            continue
        nvt = NVT.search(text)
        if nvt and len(nvt.group("reason").strip()) >= 3:
            continue
        if nvt:
            problems.append(f"'n.v.t.' zonder toelichting: {text}")
        else:
            problems.append(f"Niet afgevinkt: {text}")
    if items == 0:
        problems.append("De Definition of Done-sectie bevat geen checkboxes.")
    return problems


def main() -> int:
    problems = check(read_body())
    if problems:
        print("Definition of Done is niet volledig afgehandeld:")
        for problem in problems:
            print(f"  - {problem}")
        print("\nVink elk item af, of markeer het als 'n.v.t.: <reden>'.")
        return 1
    print("Definition of Done: alle items afgehandeld.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
