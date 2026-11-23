#!/usr/bin/env python3
"""Verzamel de gegevens over het ontwikkelproces voor het testrapport en de bewijsbundel van een release.

Gebruik: verzamel_releasegegevens.py <vorige-tag of ''> <tag> <uitvoermap>

Schrijft naar de uitvoermap:
- prs.json:  gemergde pull requests sinds de vorige tag, met auteur, reviewers en goedkeuringen;
- bugs.json: openstaande issues met het label `bug`.

Heeft het token geen leesrechten op pull requests of issues, dan volgt een waarschuwing en een leeg
bestand; het testrapport vermeldt dan dat deze gegevens ontbreken.
"""
import json
import subprocess
import sys
from pathlib import Path

import gbo_gh


def commits(previous: str, tag: str) -> list[str]:
    revision = f"{previous}..{tag}" if previous else tag
    output = subprocess.run(["git", "rev-list", "--first-parent", revision],
                            capture_output=True, text=True, check=True).stdout
    return output.split()


def merged_prs(shas: list[str]) -> list[dict]:
    seen: dict[int, dict] = {}
    for sha in shas:
        for pr in gbo_gh.api(f"repos/{gbo_gh.repo()}/commits/{sha}/pulls") or []:
            if pr["number"] in seen or not pr.get("merged_at"):
                continue
            reviews = gbo_gh.api(f"repos/{gbo_gh.repo()}/pulls/{pr['number']}/reviews", paginate=True)
            approvers = sorted({r["user"]["login"] for r in reviews
                                if r.get("state") == "APPROVED" and r.get("user")})
            reviewers = sorted({r["user"]["login"] for r in reviews if r.get("user")})
            seen[pr["number"]] = {
                "number": pr["number"],
                "title": pr["title"],
                "url": pr["html_url"],
                "author": pr["user"]["login"],
                "merged_at": pr["merged_at"],
                "merge_commit": pr.get("merge_commit_sha"),
                "reviewers": reviewers,
                "approvers": approvers,
                "labels": sorted(label["name"] for label in pr.get("labels", [])),
            }
    return sorted(seen.values(), key=lambda pr: pr["number"])


def open_bugs() -> list[dict]:
    items = gbo_gh.gh_json("issue", "list", "--repo", gbo_gh.repo(), "--label", "bug", "--state", "open",
                           "--limit", "1000", "--json", "number,title,url,labels,createdAt") or []
    return [{"number": i["number"], "title": i["title"], "url": i["url"], "created_at": i["createdAt"],
             "labels": sorted(label["name"] for label in i["labels"])} for i in items]


def write(path: Path, collect, description: str) -> None:
    try:
        data = collect()
    except RuntimeError as error:
        print(f"::warning::{description} niet opgehaald: {error}")
        data = None
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    previous, tag, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    write(out / "prs.json", lambda: merged_prs(commits(previous, tag)), "Pull requests")
    write(out / "bugs.json", open_bugs, "Openstaande bugs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
