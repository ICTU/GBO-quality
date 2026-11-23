# Changelog — GBO-quality

Alle noemenswaardige wijzigingen in dit project worden bijgehouden in dit bestand.

De indeling is gebaseerd op [Keep a Changelog](https://keepachangelog.com/nl/1.0.0/).
De versienummering volgt [Semantic Versioning](https://semver.org/lang/nl/).

## [Niet uitgebracht]

### Toegevoegd

- Repository opgezet conform de [ICTU GitHub policy](https://github.com/ICTU/github-policy):
  README, LICENSE (EUPL-1.2), CODE_OF_CONDUCT, CONTRIBUTING, SECURITY, CHANGELOG en publiccode.yml.
- ICTU Kwaliteitsaanpak Softwareontwikkeling v5.4.1 als bron (`bronnen-orig/`, `bronnen-md/`).
- Eerste opzet van de kwaliteitsaanpak voor GBO: kwaliteitsplan, maatregelenmapping (M01-M35),
  ADR's, herbruikbare workflows (quality-ci, pr-checks, dynamic-scans, release, self-ci), templates
  voor componentrepositories, controlescripts (DoD, traceerbaarheid), Claude Code-skill en hooks,
  en de inrichting van Quality-time.
- `AGENTS.md` met de gedeelde instructies voor AI-codeerassistenten, in deze repository en in de
  templates; `CLAUDE.md` importeert dit bestand. Regels toegevoegd over het gebruik van bronnen-md/ en
  bronvermelding in docs/.
- Kwaliteitsplan §8 *Informatiebeveiliging*: invulling van de BIO2 v1.3 en NEN-EN-ISO/IEC
  27001:2023/27002:2022 voor de ontwikkeling (risicoanalyse, architectuurprincipes, kwetsbaarheden-
  beheer, toegang, leveranciersketen, logging, cryptografie, overdracht naar beheer, kennis).
  AI-ondersteund ontwikkelen is nu §9. Mapping van de relevante beheersmaatregelen en
  BIO2-overheidsmaatregelen in `docs/maatregelen-mapping.md`.
- `templates/SECURITY.md` met een meldpunt voor kwetsbaarheden voor componentrepositories.
- Testrapport en bewijsbundel bij elke release (`release.yml`): tests op de getagde versie (een falende
  test houdt de release tegen), traceerbaarheid van logische testgevallen, kwetsbaarheden en
  uitzonderingen, gemergde PR's met reviewers, openstaande bugs en rollbackinstructie. De bundel
  (`bewijs-<versie>.zip`) krijgt een SHA-256-manifest en build-provenance. Nieuwe inputs: `quality-ref`,
  `test-command`, `junit-paden`, `testgevallen-map`, `ltc-patroon`, `rollback-bestand` en `tag-patroon`.
  **Let op:** de release-job vraagt nu ook `pull-requests: read` en `issues: read`; een aanroepende
  workflow moet die rechten geven (zie `templates/.github/workflows/release.yml`).
- Kwaliteitskalender en periodieke controles (`periodieke-controles.yml`, wekelijks): issues met
  checklist en deadline voor periodieke taken uit `.github/kwaliteitskalender.yml`, het label `te-laat`
  na de deadline, een issue per kwetsbaarheid (critical/high) dat automatisch heropent en sluit, en een
  toegangscontrole op MFA, beheerders en bescherming van `main`.
- Templates: `docs/rollback.md`, `docs/testgevallen/README.md`, kwaliteitskalender en `periodiek.yml`;
  `.trivyignore` met vervaldatum (`exp:`). Kwaliteitsplan §6 beschrijft kalender, periodieke controles en
  bewijs per release.
- Slimmere DoD-check: voorwaardelijke DoD-items (`<!-- dod:sleutel -->`) vervallen automatisch als
  de PR de paden uit de nieuwe input `dod-regels` van `pr-checks.yml` niet raakt. Het PR-template bevat
  alleen nog items die een mens moet beoordelen; wat pipeline en branch protection borgen en de demo
  (sprint review) zijn eruit. Kwaliteitsplan §3 beschrijft de borging per DoD-item en voegt het bijwerken
  van de risicoanalyse toe. Achterwaarts compatibel: zonder `dod-regels` werkt de check als voorheen.
- Normsamenvatting en review-checklist van de Claude Code-skill aangevuld (hersteltermijn,
  pentest, logging, cryptografie, MFA, pseudonimisering).
