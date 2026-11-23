# GBO-quality

Centrale kwaliteitsafspraken, pipeline-templates en ontwikkeltooling voor de software van het programma
[Gemeenschappelijke Bronontsluiting (GBO)](https://ictu.github.io/GBO/): de referentiecomponenten voor
bronhouders en de centrale voorzieningen.

Deze repository vertaalt de [ICTU Kwaliteitsaanpak Softwareontwikkeling](https://ictu.github.io/Kwaliteitsaanpak/)
(versie 5.4.1, zie ook [bronnen-md](bronnen-md/ICTU-Kwaliteitsaanpak.md)) naar concrete, herbruikbare afspraken en automatisering. Het doel: ontwikkelaars voldoen aan de
Kwaliteitsaanpak zonder telkens het handboek te hoeven raadplegen.

> **Status:** startversie (v0). De aanvullende eisen van RINIS zijn nog niet bekend en nog niet verwerkt;
> zie [docs/kwaliteitsplan.md](docs/kwaliteitsplan.md#open-punten).

## Uitgangspunt: drie lagen

| Laag | Wat | Waar | Garantie |
|---|---|---|---|
| 1. Pipeline | Builds, tests, scans en quality gates die een merge blokkeren | `.github/workflows/` (herbruikbaar) | Afdwingend |
| 2. Werkafspraken | PR-template met Definition of Done, CODEOWNERS, branch protection, traceerbaarheid | `templates/` | Afdwingend via branch protection en DoD-check |
| 3. AI-assistent | Claude Code-skill en hooks die helpen de afspraken na te leven | `claude/` | Ondersteunend, nooit de enige controle |

De garantie komt uit laag 1 en 2. De skill in laag 3 helpt om sneller en vollediger te werken, maar een
merge mag nooit afhangen van het wel of niet gebruiken ervan.

## Inhoud

```
docs/
  kwaliteitsplan.md          Normen, Definition of Ready/Done, werkwijze (bron van waarheid)
  maatregelen-mapping.md     Per ICTU-maatregel (M01-M35): hoe GBO hem invult en waar
  repo-aansluiten.md         Stappenplan om een GBO-repository aan te sluiten
  adr/                       Architectuurbeslissingen over deze kwaliteitsaanpak
.github/workflows/
  quality-ci.yml             Herbruikbaar: pre-commit, tests, SonarQube, Trivy, SBOM, Dependency-Track
  pr-checks.yml              Herbruikbaar: traceerbaarheid (story-ID) en Definition of Done
  dynamic-scans.yml          Herbruikbaar: ZAP-baseline en axe-toegankelijkheidstest tegen een draaiende omgeving
  release.yml                Herbruikbaar: release notes, SBOM, testrapport, bewijsbundel en build-provenance bij een tag
  periodieke-controles.yml   Herbruikbaar: kwaliteitskalender, kwetsbaarheden-issues en toegangscontrole (wekelijks)
  self-ci.yml                Controleert deze repository zelf
scripts/
  check_dod.py               Controleert of alle DoD-items in de PR afgevinkt of als n.v.t. gemarkeerd zijn
  check_traceability.py      Controleert of een PR naar een story of issue verwijst
  testrapport.py             Maakt het testrapport van een release
  verzamel_releasegegevens.py  Haalt gemergde PR's met reviewers en openstaande bugs op
  kwaliteitskalender.py      Maakt issues voor periodieke taken en markeert te late issues
  kwetsbaarheden.py          Maakt, heropent en sluit issues per kwetsbaarheid
  toegangscontrole.py        Controleert MFA, beheerders en bescherming van main
  aansluiten.sh              Kopieert de templates naar een GBO-repository
templates/                   Bestanden die in elke GBO-repository komen (o.a. AGENTS.md en CLAUDE.md)
AGENTS.md                    Instructies voor AI-codeerassistenten in deze repository
claude/                      Claude Code-skill en hooks (worden via aansluiten.sh gekopieerd)
quality-time/                Inrichting van de kwaliteitsrapportage in Quality-time
bronnen-orig/                Originele bronbestanden (o.a. ICTU Kwaliteitsaanpak v5.4.1 in Word)
bronnen-md/                  Markdown-versies van de bronbestanden
```

## Snel starten in een GBO-repository

```bash
git clone https://github.com/ICTU/GBO-quality.git
./GBO-quality/scripts/aansluiten.sh ../mijn-gbo-component
```

Volg daarna [docs/repo-aansluiten.md](docs/repo-aansluiten.md) voor branch protection, secrets en de
koppeling met SonarQube, Dependency-Track en Quality-time.

## Versiebeheer van deze repository

GBO-repositories verwijzen naar de workflows met een tag, bijvoorbeeld
`ICTU/GBO-quality/.github/workflows/quality-ci.yml@v0`. Wijzigingen die bestaande repositories kunnen breken
krijgen een nieuwe major-tag. Zie [CHANGELOG.md](CHANGELOG.md).

De repository staat nu bij ICTU en kan later naar een omgeving van RINIS verhuizen. Verwijs daarom in
GBO-repositories alleen via de `uses:`-regels en `aansluiten.sh` naar deze repo, zodat een verhuizing op
een beperkt aantal plekken hoeft te worden doorgevoerd.

## Relatie met de andere GBO-repositories

| Repository | Inhoud |
|---|---|
| [ICTU/GBO](https://github.com/ICTU/GBO) | Startpunt van de GBO-documentatie |
| [ICTU/GBO-GO](https://github.com/ICTU/GBO-GO) | Globaal Ontwerp |
| [ICTU/GBO-PSA](https://github.com/ICTU/GBO-PSA) | Projectstartarchitectuur |
| [ICTU/GBO-TO](https://github.com/ICTU/GBO-TO) | Technisch Ontwerp: wat er gebouwd wordt |
| [ICTU/GBO-Semantiek](https://github.com/ICTU/GBO-Semantiek) | Architectuur voor semantiek |
| [ICTU/GBO-demo](https://github.com/ICTU/GBO-demo) | Referentie-implementatie (demo-omgeving) |

Het Technisch Ontwerp (GBO-TO) is de belangrijkste bron voor wat er gemaakt wordt
en al gemaakt is in de demo-omgeving; deze repository toetst die ontwikkeling.

## Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md) en de [gedragscode](CODE_OF_CONDUCT.md). Wijzigingen in normen lopen
via een pull request met review door de kwaliteitsmanager. Beveiligingsproblemen meld je volgens
[SECURITY.md](SECURITY.md).

Deze repository volgt de [ICTU GitHub policy](https://github.com/ICTU/github-policy).

## Licentie

Deze repository valt onder de [European Union Public Licence v1.2 (EUPL-1.2)](LICENSE).

## Contact

Eigenaar: ICTU - programma GBO

Contactpersoon: [Govert Claus](mailto:govert.claus@ictu.nl)

Vragen en voorstellen kun je ook als [issue](https://github.com/ICTU/GBO-quality/issues) indienen.
