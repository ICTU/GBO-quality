#!/usr/bin/env python3
"""Controleer of alle Definition of Done-items in een PR-beschrijving zijn afgehandeld.

Leest de PR-beschrijving uit de omgevingsvariabele PR_BODY (of uit een bestand als eerste argument).
Alleen checkboxes tussen de markeringen <!-- dod:start --> en <!-- dod:end --> tellen mee.
Een item is afgehandeld als het is afgevinkt ([x]) of de tekst "n.v.t." bevat met een toelichting.

Voorwaardelijke items
---------------------
Een item kan een sleutel dragen, bijvoorbeeld:

    - [ ] Conformancetests bijgewerkt <!-- dod:koppelvlak -->

DOD_RULES koppelt sleutels aan paden in de repository, één regel per sleutel:

    koppelvlak: api/** **/*.graphql
    ui: frontend/**

CHANGED_FILES bevat de gewijzigde bestanden van de PR (één per regel). Raakt de PR geen pad van de
sleutel, dan is het item automatisch niet van toepassing en hoeft de ontwikkelaar er niets mee.
Raakt de PR wel zo'n pad, of is er geen regel of geen lijst met gewijzigde bestanden, dan geldt het
item zoals elk ander item.

Patronen: `*` en `?` binnen één map, `**` over mappen heen. Een patroon zonder `/` geldt in elke map.

Exitcode 0: alles afgehandeld. Exitcode 1: open items of geen DoD-sectie gevonden.
"""
import os
import re
import sys

START = "<!-- dod:start -->"
END = "<!-- dod:end -->"
CHECKBOX = re.compile(r"^\s*[-*]\s*\[(?P<state>[ xX])\]\s*(?P<text>.+)$")
NVT = re.compile(r"\bn\.?v\.?t\.?\b\s*[:\-–]?\s*(?P<reason>.*)", re.IGNORECASE)
KEY = re.compile(r"<!--\s*dod:(?P<key>[\w-]+)\s*-->")
RULE = re.compile(r"^\s*(?P<key>[\w-]+)\s*:\s*(?P<patterns>.*)$")


def read_body() -> str:
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as handle:
            return handle.read()
    return os.environ.get("PR_BODY", "")


def parse_rules(text: str) -> dict[str, list[str]]:
    rules: dict[str, list[str]] = {}
    for line in text.splitlines():
        line = line.split("#", 1)[0]
        match = RULE.match(line)
        if match:
            patterns = match.group("patterns").replace(",", " ").split()
            rules.setdefault(match.group("key"), []).extend(patterns)
    return rules


def glob_to_regex(pattern: str) -> re.Pattern:
    pattern = pattern.strip()
    while pattern.startswith("./"):
        pattern = pattern[2:]
    pattern = pattern.lstrip("/")
    if "/" not in pattern:
        pattern = "**/" + pattern
    regex = ""
    i = 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            regex += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            regex += ".*"
            i += 2
        elif pattern[i] == "*":
            regex += "[^/]*"
            i += 1
        elif pattern[i] == "?":
            regex += "[^/]"
            i += 1
        else:
            regex += re.escape(pattern[i])
            i += 1
    return re.compile(regex + r"\Z")


def applies(key: str, rules: dict[str, list[str]], changed: list[str] | None) -> bool:
    if changed is None or key not in rules:
        return True
    regexes = [glob_to_regex(p) for p in rules[key]]
    return any(r.match(path) for path in changed for r in regexes)


def check(body: str, rules: dict[str, list[str]] | None = None,
          changed: list[str] | None = None) -> tuple[list[str], list[str]]:
    """Geeft (problemen, automatisch niet van toepassing) terug."""
    rules = rules or {}
    if START not in body or END not in body:
        return ["De PR-beschrijving bevat geen Definition of Done-sectie. Gebruik het PR-template."], []
    section = body.split(START, 1)[1].split(END, 1)[0]
    problems: list[str] = []
    skipped: list[str] = []
    items = 0
    for line in section.splitlines():
        match = CHECKBOX.match(line)
        if not match:
            continue
        items += 1
        key = KEY.search(match.group("text"))
        text = KEY.sub("", match.group("text")).strip()
        if match.group("state").lower() == "x":
            continue
        if key and not applies(key.group("key"), rules, changed):
            skipped.append(text)
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
    return problems, skipped


def read_changed() -> list[str] | None:
    if "CHANGED_FILES" not in os.environ:
        return None
    return [line.strip() for line in os.environ["CHANGED_FILES"].splitlines() if line.strip()]


def main() -> int:
    problems, skipped = check(read_body(), parse_rules(os.environ.get("DOD_RULES", "")), read_changed())
    if skipped:
        print("Automatisch niet van toepassing (de PR raakt de bijbehorende paden niet):")
        for text in skipped:
            print(f"  - {text}")
        print()
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
