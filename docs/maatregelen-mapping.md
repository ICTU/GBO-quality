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
| M26 | Periodieke securitybeoordeling | Pentest en code review per grote release, ≥ 2× per jaar | Handmatig | `kwaliteitsplan.md` §4, Quality-time |
| M27 | Archivering bij afsluiting | Checklist bij fase-einde | Handmatig | Projectorganisatie |
| M28 | Self-assessment | Checklist in Quality-time | Handmatig | `quality-time/README.md` |
| M29 | Interne dienstverlening vooraf | Afspraken met ISD/ISE | ICTU + Proces | Open punt 3 |
| M30 | Risicomanagement | Risicolog | Proces | Projectorganisatie |
| M32 | Due diligence bestaande software | Bij hergebruik van bestaande componenten (bijv. FSC, OOTS-V) | Handmatig | Per component |
| M33 | Gezamenlijke self-assessment | — | ICTU | — |
| M34 | Beheerste overdracht | Relevant bij verhuizing naar RINIS of overdracht aan beheerder: NPR 5325-criteria | Handmatig | Bij overdracht |
| M35 | Agile architectuur | SAD bijwerken; ADR's per beslissing | Proces | ADR's in componentrepo's |
