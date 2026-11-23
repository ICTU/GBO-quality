"""Hulpfuncties rond de GitHub-CLI (`gh`) voor de GBO-scripts.

`gh` leest het token uit GH_TOKEN (voor issues en labels GH_ISSUE_TOKEN, als dat gezet is); de
repository uit GITHUB_REPOSITORY (owner/naam).
"""
import json
import os
import re
import subprocess
from datetime import date

DEADLINE = re.compile(r"^\*\*Uiterlijk:\*\*\s*(?P<datum>\d{4}-\d{2}-\d{2})", re.MULTILINE)


def repo() -> str:
    return os.environ["GITHUB_REPOSITORY"]


def gh(*args: str, input_text: str | None = None) -> str:
    env = None
    # Issues en labels mogen met een ander token (GH_ISSUE_TOKEN) dan het lezen van de organisatie.
    if args and args[0] in ("issue", "label") and os.environ.get("GH_ISSUE_TOKEN"):
        env = {**os.environ, "GH_TOKEN": os.environ["GH_ISSUE_TOKEN"]}
    result = subprocess.run(["gh", *args], input=input_text, capture_output=True, text=True, check=False, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} mislukt: {result.stderr.strip()}")
    return result.stdout


def gh_json(*args: str):
    output = gh(*args)
    return json.loads(output) if output.strip() else None


def api(path: str, paginate: bool = False):
    args = ["api", "-H", "Accept: application/vnd.github+json", path]
    if paginate:
        args += ["--paginate", "--slurp"]
        pages = gh_json(*args) or []
        return [item for page in pages for item in (page if isinstance(page, list) else [page])]
    return gh_json(*args)


def ensure_label(name: str, color: str = "ededed", description: str = "") -> None:
    gh("label", "create", name, "--repo", repo(), "--color", color, "--description", description, "--force")


def issues(label: str, state: str = "all") -> list[dict]:
    return gh_json("issue", "list", "--repo", repo(), "--label", label, "--state", state,
                   "--limit", "1000", "--json", "number,title,body,state,labels") or []


def create_issue(title: str, body: str, labels: list[str], assignees: list[str] | None = None) -> str:
    args = ["issue", "create", "--repo", repo(), "--title", title, "--body-file", "-"]
    for label in labels:
        args += ["--label", label]
    for assignee in assignees or []:
        args += ["--assignee", assignee.lstrip("@")]
    return gh(*args, input_text=body).strip()


def deadline(body: str) -> date | None:
    match = DEADLINE.search(body or "")
    return date.fromisoformat(match.group("datum")) if match else None
