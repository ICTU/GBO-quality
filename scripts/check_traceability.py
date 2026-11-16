#!/usr/bin/env python3
"""Controleer of een pull request naar een story of issue verwijst (ICTU-maatregel M03).

Leest PR_TITLE en PR_BODY uit de omgeving. Het patroon is instelbaar via TRACE_PATTERN
(standaard: Jira-sleutels zoals GBO-123, of GitHub-issues zoals #45 of ICTU/repo#45).
PR's van bots (Dependabot) en PR's met het label 'geen-story' worden overgeslagen via de workflow.
"""
import os
import re
import sys

DEFAULT_PATTERN = r"\b[A-Z][A-Z0-9]+-\d+\b|(?:[\w.-]+/[\w.-]+)?#\d+\b"


def main() -> int:
    pattern = re.compile(os.environ.get("TRACE_PATTERN") or DEFAULT_PATTERN)
    title = os.environ.get("PR_TITLE", "")
    body = os.environ.get("PR_BODY", "")
    found = sorted(set(pattern.findall(f"{title}\n{body}")))
    if found:
        print(f"Traceerbaarheid: PR verwijst naar {', '.join(found)}.")
        return 0
    print("Traceerbaarheid: de PR verwijst niet naar een story of issue.")
    print("Noem de story in de titel of beschrijving, bijvoorbeeld 'GBO-123' of 'Closes #45'.")
    print(f"Gebruikt patroon: {pattern.pattern}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
