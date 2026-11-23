# Mapping ICTU-maatregelen naar GBO

Per maatregel uit de [ICTU Kwaliteitsaanpak](https://ictu.github.io/Kwaliteitsaanpak/) v5.4.1: hoe GBO hem
invult en waar dat zichtbaar is. Gebruik dit overzicht bij de self-assessment (M28).

**Borging:** *Auto* = afgedwongen door de pipeline · *Proces* = werkafspraak, zichtbaar in tooling ·
*Handmatig* = periodieke menselijke activiteit · *ICTU* = verantwoordelijkheid van de ICTU-organisatie,
niet van het project.

| Maatregel | Kern | GBO-invulling | Borging | Waar |
|---|---|---|---|---|
| M01 | Producten per fase | Voorfaseproducten op ictu.github.io/GBO; realisatieproducten: release, SBOM, release notes, testrapportages | Proces + Auto | `release.yml`, GBO-documentatiesites |
| M02 | Continu bewaken kwaliteitsnormen | Normen in kwaliteitsplan §2; Quality-time meet continu | Auto + Proces | `kwaliteitsplan.md`, `quality-time/` |
| M03 | Traceerbaarheid eisen ↔ tests | Story-ID in PR; LTC-ID in testen | Auto (PR) + Proces (tests) | `pr-checks.yml`, `check_traceability.py` |
| M04 | Geautomatiseerde regressietests | Volledige testset per PR; dekkingsnorm in Quality-time | Auto | `quality-ci.yml` |
| M05 | Iteratief en incrementeel (Scrum) | Scrum, DoR en DoD | Proces | `kwaliteitsplan.md` §3 |
| M07 | Continuous delivery pipeline | Herbruikbare workflows voor build, test, scans, release | Auto | `.github/workflows/` |
| M08 | Technische schuld | Markeren in Quality-time; ~10% sprintcapaciteit | Proces | `kwaliteitsplan.md` §6 |
| M10 | Wekelijks projectoverleg | Agenda incl. kwaliteit en risico's | Proces | Projectorganisatie |
| M11 | Beheer Kwaliteitsaanpak | — | ICTU | — |
| M12 | Publicatie Kwaliteitsaanpak | — | ICTU | — |
| M14 | Voorfase | GO, PSA, TO, TR op ictu.github.io | Proces | GBO-documentatiesites |
| M16 | Verplichte tools | GitHub (gelijkwaardig aan GitLab), GitHub Actions, SonarQube, Trivy, Dependency-Track, ZAP, axe, CycloneDX, Quality-time | Auto | `quality-ci.yml`, `dynamic-scans.yml` |
| M18 | Ondersteuning tools | — | ICTU | — |
| M19 | Afgeschermde omgevingen | Aan te vragen bij ICTU ISD | ICTU + Proces | Open punt 3 |
| M21 | Kwaliteit bij inzet medewerkers | — | ICTU | — |
| M23 | Kennis van de Kwaliteitsaanpak | Onboarding via deze repository | Proces | `README.md` |
| M26 | Periodieke securitybeoordeling | Pentest en code review per grote release, ≥ 2× per jaar; internetfacing componenten bij elke release | Handmatig | `kwaliteitsplan.md` §4 en §8.4, Quality-time |
| M27 | Archivering bij afsluiting | Checklist bij fase-einde | Handmatig | Projectorganisatie |
| M28 | Self-assessment | Checklist in Quality-time | Handmatig | `quality-time/README.md` |
| M29 | Interne dienstverlening vooraf | Afspraken met ISD/ISE | ICTU + Proces | Open punt 3 |
| M30 | Risicomanagement | Risicolog | Proces | Projectorganisatie |
| M32 | Due diligence bestaande software | Bij hergebruik van bestaande componenten (bijv. FSC, OOTS-V) | Handmatig | Per component |
| M33 | Gezamenlijke self-assessment | — | ICTU | — |
| M34 | Beheerste overdracht | Relevant bij verhuizing naar RINIS of overdracht aan beheerder: NPR 5325-criteria | Handmatig | Bij overdracht |
| M35 | Agile architectuur | SAD bijwerken; ADR's per beslissing | Proces | ADR's in componentrepo's |

## Beheersmaatregelen informatiebeveiliging

Per beheersmaatregel uit NEN-EN-ISO/IEC 27002:2022 (Annex A van NEN-EN-ISO/IEC 27001:2023) die de
ontwikkeling van GBO-software raakt, met de verplichte BIO2-overheidsmaatregelen (BIO2 v1.3, deel 2).
Gebruik dit overzicht als bijdrage aan de Verklaring van toepasselijkheid van de organisatie die het ISMS
beheert (zie `kwaliteitsplan.md` §8.1). Beheersmaatregelen die vooral de beheer- of hostingorganisatie
raken (zoals fysieke beveiliging, netwerken, back-up en monitoring in productie) staan hier niet in.

| Beheersmaatregel | BIO2-overheidsmaatregel | GBO-invulling | Borging | Waar |
|---|---|---|---|---|
| 5.8 Informatiebeveiliging in projectmanagement | 5.08.01 | Risicoanalyse en beveiligingseisen per component; beveiligingseisen in de DoR | Proces | `kwaliteitsplan.md` §3, §8.2 |
| 5.21 ICT-toeleveringsketen | 5.21.02-5.21.05 | SBOM, build-provenance en beveiligingsdocumentatie per release; end-of-life dependencies vervangen | Auto + Proces | `release.yml`, `kwaliteitsplan.md` §5, §8.6 |
| 5.23 Clouddiensten | 5.23.01 | Register van clouddiensten en tools, inclusief AI-assistenten | Handmatig | `kwaliteitsplan.md` §8.6, §9 |
| 5.32 Intellectuele eigendomsrechten | — | EUPL-1.2; licentiecontrole van dependencies in Dependency-Track | Proces | `kwaliteitsplan.md` §5 |
| 5.37 Gedocumenteerde bedieningsprocedures | — | Installatie- en beheerdocumentatie in de DoD | Proces | `kwaliteitsplan.md` §3, §8.8 |
| 7.2 Competentie (27001) | — | Onboarding en jaarlijkse training veilig programmeren | Handmatig | `kwaliteitsplan.md` §8.9 |
| 8.2 en 8.4 Toegang tot broncode | 5.17.01 (MFA) | Beschermde `main`, PR met review, CODEOWNERS, MFA, beperkte beheerrechten | Auto + Proces | `repo-aansluiten.md` stap 4, `kwaliteitsplan.md` §8.5 |
| 8.8 Technische kwetsbaarheden | 8.08.01-8.08.05 | Trivy, Dependency-Track, `SECURITY.md`; hersteltermijn 1 week bij hoog risico; pentest per release voor internetfacing | Auto + Handmatig | `quality-ci.yml`, `kwaliteitsplan.md` §2, §8.4 |
| 8.9 Configuratiebeheer | — | Vastgepinde versies; veilige standaardconfiguratie (*security by default*) | Auto + Proces | `kwaliteitsplan.md` §5, §8.3 |
| 8.11 Maskeren van gegevens | — | Pseudonimisering aantoonbaar getest | Proces | `kwaliteitsplan.md` §7 |
| 8.15 Logging | 8.15.01-8.15.04 | LDV, verplichte velden per logregel, geen BSN's of secrets in logs, overzicht van logbestanden | Proces | `kwaliteitsplan.md` §7, §8.7 |
| 8.24 Cryptografie | 8.24.01, 8.24.04 | NCSC-adviezen en Forum Standaardisatie; bewezen bibliotheken; sleutels buiten de code; tweede reviewer | Proces | `kwaliteitsplan.md` §3, §8.7 |
| 8.25 Veilige ontwikkelcyclus | — | Dit kwaliteitsplan als geheel | Proces | `kwaliteitsplan.md` |
| 8.26 Beveiligingseisen voor applicaties | — | Beveiligingseisen uit de risicoanalyse, vertaald naar logische testgevallen | Proces | `kwaliteitsplan.md` §8.2 |
| 8.27 Veilige systeemarchitectuur | 8.27.01 | Architectuurprincipes in SAD; afwijkingen in ADR | Proces | `kwaliteitsplan.md` §8.3 |
| 8.28 Veilig programmeren | — | Codeerstandaarden, review-checklist, SonarQube, gitleaks, dependencybeheer | Auto + Proces | `kwaliteitsplan.md` §2, §3, §5 |
| 8.29 Beveiligingstesten | 8.29.01 | SAST, dependency- en imagescan, ZAP, pentest; testrapport per release | Auto + Handmatig | `kwaliteitsplan.md` §4 |
| 8.30 Uitbestede ontwikkeling | 8.30.01 | Zelfde eisen voor uitbestede ontwikkeling en alternatieven van bronhouders; conformancetests | Proces | `kwaliteitsplan.md` §7, §8.6 |
| 8.31 Scheiding van omgevingen | 8.31.01-8.31.02 | Gescheiden omgevingen; niet testen in productie zonder goedkeuring | Proces | `kwaliteitsplan.md` §7, §8.8 |
| 8.32 Wijzigingsbeheer | 8.32.01-8.32.02 | PR-proces en releases; release notes, testrapport en rollbackinstructie voor de beheerder | Auto + Proces | `kwaliteitsplan.md` §3, §8.8 |
| 8.33 Testgegevens | — | Alleen synthetische testdata | Proces | `kwaliteitsplan.md` §7 |
| 8.34 Bescherming tijdens audits | — | Pentests op productie alleen na afspraak met de beheerder | Handmatig | `kwaliteitsplan.md` §8.4 |
