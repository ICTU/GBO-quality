# AGENTS.md – GBO-quality

Instructies voor AI-codeerassistenten (Claude Code, Codex, Copilot en andere) die in deze repository werken.

Deze repository bevat de centrale kwaliteitsafspraken en herbruikbare tooling voor alle GBO-software.
Zie README.md voor de opzet en docs/kwaliteitsplan.md voor de normen.

## Werken aan deze repository

- Testen: `python3 -m unittest discover -s tests -v`
- Workflows controleren: `actionlint` (brew install actionlint)
- Shellscripts controleren: `shellcheck scripts/*.sh claude/hooks/*.sh`
- Pre-commit: `pre-commit run --all-files`
- Templates proberen: `scripts/aansluiten.sh <pad-naar-testrepo> --dry-run`

## Bronnen

- Baseer kwaliteitseisen en uitspraken in docs/ op de bronnen in bronnen-md/
  (o.a. ICTU-Kwaliteitsaanpak.md, v5.4.1; maatregelen staan als kop "M01: ..." t/m "M35: ...").
  Zoek gericht op het maatregelnummer in plaats van het hele document te lezen.
  Gebruik alleen een andere bron als bronnen-md/ het antwoord niet geeft, en zeg dat dan expliciet.
- Vermeld bij elke inhoudelijke uitspraak in docs/ de bron, in de vorm
  "(bron: ICTU Kwaliteitsaanpak v5.4.1, M26)". Noem de gebruikte bronnen ook in de PR-beschrijving.
- Bewerk bronnen-orig/ en bronnen-md/ niet; dit zijn kopieën van de originelen.

## Aandachtspunten

- Wijzigingen aan herbruikbare workflows kunnen alle GBO-repositories breken. Houd inputs achterwaarts
  compatibel of verhoog de major-tag, en werk CHANGELOG.md bij.
- Normen wijzigen alleen in docs/kwaliteitsplan.md; houd de samenvatting in
  claude/skills/gbo-kwaliteit/references/normen.md en docs/maatregelen-mapping.md daarmee in lijn.
- GitHub Actions van derden vastpinnen op een commit-SHA, met de versie als commentaar.
- Kies bij versie-updates van tools een release die minstens 14 dagen oud is.
- Schrijf documentatie in het Nederlands.
- Instructies voor AI-assistenten staan in AGENTS.md; CLAUDE.md importeert dit bestand. Zet gedeelde
  instructies dus hier en niet in CLAUDE.md.
