#!/usr/bin/env bash
# Claude Code PreToolUse-hook voor Bash-commando's.
# - Blokkeert het omzeilen van git-hooks (--no-verify) en force-pushes naar main.
# - Draait pre-commit vóór een git commit, ook als de git-hook lokaal niet is geïnstalleerd.
# Exitcode 2 blokkeert het commando; de melding op stderr gaat terug naar Claude.
set -uo pipefail

input="$(cat)"
command="$(printf '%s' "$input" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || true)"

[[ -z "$command" ]] && exit 0

if [[ "$command" =~ git[[:space:]]+(commit|push).*--no-verify || "$command" =~ git[[:space:]]+commit.*[[:space:]]-n([[:space:]]|$) ]]; then
  echo "Geblokkeerd: controles omzeilen met --no-verify is niet toegestaan (GBO-kwaliteitsplan). Los de gevonden problemen op of vraag de gebruiker." >&2
  exit 2
fi

if [[ "$command" =~ git[[:space:]]+push && "$command" =~ (--force|[[:space:]]-f([[:space:]]|$)) && "$command" =~ (main|master) ]]; then
  echo "Geblokkeerd: force-push naar main is niet toegestaan." >&2
  exit 2
fi

if [[ "$command" =~ git[[:space:]]+commit ]]; then
  if ! command -v pre-commit >/dev/null 2>&1; then
    echo "Let op: pre-commit is niet geïnstalleerd (brew install pre-commit). Controles zijn niet lokaal gedraaid." >&2
    exit 0
  fi
  if [[ ! -f "${CLAUDE_PROJECT_DIR:-.}/.pre-commit-config.yaml" ]]; then
    exit 0
  fi
  cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
  if ! output="$(pre-commit run 2>&1)"; then
    {
      echo "pre-commit vond problemen; de commit is tegengehouden. Los ze op en probeer opnieuw:"
      echo "$output" | tail -n 60
    } >&2
    exit 2
  fi
fi

exit 0
