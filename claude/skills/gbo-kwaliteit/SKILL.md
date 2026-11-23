---
name: gbo-kwaliteit
description: Werkwijze voor kwaliteit in GBO-repositories volgens de ICTU Kwaliteitsaanpak. Gebruik bij elke commit, bij het voorbereiden of reviewen van een pull request, bij het wijzigen van een API-schema, koppelvlak of autorisatieregel, bij het toevoegen van dependencies en bij het voorbereiden van een release.
---

# GBO-kwaliteit

Deze skill helpt de afspraken uit het GBO-kwaliteitsplan na te leven. De pipeline in
ICTU/GBO-quality dwingt de normen af; deze skill zorgt dat het werk daar in één keer doorheen komt
en dat de documentatie en traceerbaarheid kloppen.

Normen staan in `references/normen.md`. De review-checklist staat in `references/review-checklist.md`.

## Uitgangspunten

- Omzeil nooit een controle (`--no-verify`, overgeslagen tests, verlaagde drempels, uitzonderingen in
  `.trivyignore` of SonarQube) zonder dat de gebruiker daar expliciet om vraagt. Leg dan de reden vast.
- Vink een Definition of Done-item alleen af als je het zelf hebt gecontroleerd. Wat je niet kunt
  controleren (bijv. een menselijke review of een demo), laat je open en benoem je voor de gebruiker.
- Gebruik alleen synthetische testdata; nooit echte BSN's of persoonsgegevens.

## Voor een commit

1. Draai de tests van de component (zie AGENTS.md) en `pre-commit run`.
2. Los gevonden problemen op in plaats van ze te onderdrukken.
3. Schrijf een Conventional Commit-bericht: `type(scope): omschrijving`. Gebruik `feat`, `fix`,
   `perf`, `security`, `docs`, `refactor`, `test`, `ci`, `chore`. Zet `BREAKING CHANGE:` in de body
   bij een niet-compatibele wijziging van een koppelvlak.

## Pull request voorbereiden

1. Stel vast naar welke story of welk issue de PR verwijst. Vraag het aan de gebruiker als het
   onbekend is; verzin geen ID.
2. Bepaal de documentatie-impact met de tabel hieronder en werk de documentatie bij.
3. Controleer de wijziging met `references/review-checklist.md` en verwerk wat je vindt.
4. Controleer of nieuwe of gewijzigde tests het ID van het logische testgeval dragen.
5. Vul het PR-template in (`.github/pull_request_template.md`):
   - beschrijf wat en waarom, en hoe getest;
   - vink alleen gecontroleerde items af; markeer niet-relevante items als `n.v.t.: <reden>`;
   - items met een markering `<!-- dod:... -->` laat je ongemoeid als de PR de paden uit `dod-regels`
     in `.github/workflows/ci.yml` niet raakt: de pipeline stelt dan zelf vast dat ze niet gelden;
   - benoem onder "Aandachtspunten voor de reviewer" de risico's en wat je niet kon controleren.
6. Maak de PR aan met `gh pr create` als de gebruiker dat wil.

### Documentatie-impact

| Gewijzigd | Bijwerken |
|---|---|
| GraphQL- of OpenAPI-schema, berichtformaat | Schema-documentatie, conformancetests, release notes; bij breaking change: aankondiging |
| Autorisatie: policies, PEP/PDP, AuthZEN-aanroepen | Policydocumentatie, tests per beleidsregel; tweede reviewer met securitykennis |
| Logging | Controleer LDV-conformiteit en dat er geen leesbare BSN's worden gelogd |
| Configuratie-opties, omgevingsvariabelen | README of configuratiedocumentatie, voorbeeldconfiguratie |
| Deployment (Dockerfile, Helm, compose) | Installatie- en beheerdocumentatie |
| Keuze met invloed op architectuur of meerdere componenten | Nieuwe ADR in `docs/adr/`; melden voor het SAD |
| Nieuwe dependency | Licentie controleren (compatibel met de licentie van de repo), onderhoudsstatus, versie vastpinnen |
| Gebruikersinterface | Toegankelijkheid (WCAG 2.2 AA), axe-test |

## Release voorbereiden

1. Controleer dat `main` groen is en dat er geen open kritieke kwetsbaarheden zijn.
2. Bepaal het versienummer volgens semver op basis van de commits sinds de vorige tag
   (`git log $(git describe --tags --abbrev=0)..HEAD --oneline`).
3. Controleer dat `docs/rollback.md` klopt voor deze release en dat open issues met het label
   `kwetsbaarheid` een vastgelegde risicoafweging hebben.
4. Laat de gebruiker de tag zetten (`git tag vX.Y.Z && git push origin vX.Y.Z`); de release-workflow
   maakt release notes, SBOM, testrapport, bewijsbundel en provenance.
5. Stel daarna een concept op van de informatie voor het vrijgaveadvies, met het testrapport van de
   release als basis: gerealiseerde eisen en hoe getoetst, openstaande bugs, afwijkingen in de
   kwaliteitsrapportage met risico's, overige risico's.
