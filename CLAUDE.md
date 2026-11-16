# CLAUDE.md – GBO-quality

Deze repository bevat de centrale kwaliteitsafspraken en herbruikbare tooling voor alle GBO-software.
Zie README.md voor de opzet en docs/kwaliteitsplan.md voor de normen.

## Werken aan deze repository

- Testen: `python3 -m unittest discover -s tests -v`
- Workflows controleren: `actionlint` (brew install actionlint)
- Shellscripts controleren: `shellcheck scripts/*.sh claude/hooks/*.sh`
- Templates proberen: `scripts/aansluiten.sh <pad-naar-testrepo> --dry-run`

## Aandachtspunten

- Wijzigingen aan herbruikbare workflows kunnen alle GBO-repositories breken. Houd inputs
  achterwaarts compatibel of verhoog de major-tag, en werk CHANGELOG.md bij.
- Normen wijzigen alleen in docs/kwaliteitsplan.md; houd de samenvatting in
  claude/skills/gbo-kwaliteit/references/normen.md en docs/maatregelen-mapping.md daarmee in lijn.
- GitHub Actions van derden vastpinnen op een commit-SHA, met de versie als commentaar.
- Kies bij versie-updates van tools een release die minstens 14 dagen oud is.
- Schrijf documentatie in het Nederlands.
