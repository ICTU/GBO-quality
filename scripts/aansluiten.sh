#!/usr/bin/env bash
# Kopieer de GBO-templates naar een componentrepository zonder bestaande bestanden te overschrijven.
# Gebruik: scripts/aansluiten.sh <pad-naar-repository> [--dry-run]
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Gebruik: $0 <pad-naar-repository> [--dry-run]" >&2
  exit 1
fi

target="$1"
dry_run="${2:-}"
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$target/.git" ]]; then
  echo "Fout: $target is geen git-repository." >&2
  exit 1
fi

copied=0
skipped=0

copy_tree() {
  local source_dir="$1" dest_dir="$2"
  while IFS= read -r -d '' file; do
    local rel="${file#"$source_dir"/}"
    local dest="$dest_dir/$rel"
    if [[ -e "$dest" ]]; then
      echo "  overgeslagen (bestaat al): $rel"
      skipped=$((skipped + 1))
      continue
    fi
    echo "  toevoegen: $rel"
    copied=$((copied + 1))
    if [[ "$dry_run" != "--dry-run" ]]; then
      mkdir -p "$(dirname "$dest")"
      cp "$file" "$dest"
    fi
  done < <(find "$source_dir" -type f -print0 | sort -z)
}

echo "Templates naar $target:"
copy_tree "$root/templates" "$target"
echo "Claude Code-skill en hooks naar $target/.claude:"
copy_tree "$root/claude" "$target/.claude"

if [[ "$dry_run" != "--dry-run" && -d "$target/.claude/hooks" ]]; then
  chmod +x "$target"/.claude/hooks/*.sh 2>/dev/null || true
fi

echo
echo "Klaar: $copied toegevoegd, $skipped overgeslagen."
echo "Volgende stap: zie docs/repo-aansluiten.md (stap 2 t/m 6)."
