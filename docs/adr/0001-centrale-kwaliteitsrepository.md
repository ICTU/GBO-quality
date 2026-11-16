# ADR-0001: Centrale repository voor kwaliteitsafspraken en pipelines

- Status: voorgesteld
- Datum: 2026-11-16

## Context

GBO bestaat uit meerdere softwarecomponenten in afzonderlijke repositories. Al deze componenten moeten
voldoen aan de ICTU Kwaliteitsaanpak en, zodra bekend, aan de eisen van RINIS. Als elke repository zijn eigen
pipeline en afspraken onderhoudt, lopen ze uit elkaar en kost een wijziging van een norm veel werk.

## Besluit

We beheren normen, Definition of Done, herbruikbare GitHub Actions-workflows, repository-templates en de
Claude Code-skill centraal in `ICTU/GBO-quality`. Componentrepositories roepen de workflows aan via een
versietag en krijgen de templates via `scripts/aansluiten.sh`.

## Gevolgen

- Een wijziging in normen of pipeline gebeurt op één plek en wordt via een versietag uitgerold.
- Componentrepositories zijn afhankelijk van deze repository; breaking changes vragen een nieuwe major-tag.
- De repository kan later naar een omgeving van RINIS verhuizen; dan moeten de `uses:`-verwijzingen in de
  componentrepositories worden bijgewerkt.
- Gekopieerde templates lopen na verloop van tijd uit de pas met het origineel. `aansluiten.sh` kan opnieuw
  worden gedraaid om ontbrekende bestanden aan te vullen; verschillen worden bij de self-assessment bekeken.
