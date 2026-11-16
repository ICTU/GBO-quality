# AGENTS.md

Instructies voor AI-codeerassistenten (Claude Code, Codex, Copilot en andere) die in deze repository werken.

## Over deze component

<!-- Vul in: wat doet deze component, welke rol in GBO (referentiecomponent of centrale voorziening),
welke GBO-afspraken en standaarden implementeert hij (bijv. GraphQL-bronontsluiting, AuthZEN, LDV, FSC)? -->

## Lokaal werken

<!-- Vul in: hoe installeer je dependencies, hoe draai je de tests, hoe start je de component? -->

```bash
# installeren:
# testen:
# starten:
```

## Kwaliteitsafspraken

Deze repository volgt het GBO-kwaliteitsplan (https://github.com/ICTU/GBO-quality/blob/main/docs/kwaliteitsplan.md),
gebaseerd op de ICTU Kwaliteitsaanpak.

Harde regels:

- Draai de tests en `pre-commit run` voordat je een wijziging als klaar beschouwt.
- Gebruik Conventional Commits (`feat:`, `fix:`, `docs:` ...) en noem de story (bijv. `GBO-123`) in de PR.
- Omzeil nooit controles: geen `--no-verify`, geen uitgeschakelde tests, geen verlaagde drempels.
  Kan iets niet, meld dat dan aan de gebruiker.
- Gebruik geen echte persoonsgegevens of BSN's, ook niet in tests; gebruik synthetische testdata.
- Vink in de Definition of Done van het PR-template alleen items af die je echt hebt gecontroleerd.
