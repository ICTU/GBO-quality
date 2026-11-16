# Kwaliteitsplan GBO-software

Dit document is de bron van waarheid voor de kwaliteitsnormen en werkafspraken van alle GBO-softwarecomponenten.
Het volgt de opbouw van het [ICTU-template kwaliteitsplan](https://ictu.github.io/Kwaliteitsaanpak/) en de
[ICTU Kwaliteitsaanpak](https://ictu.github.io/Kwaliteitsaanpak/) versie 5.4.1. Waar dit plan iets niet regelt,
geldt de Kwaliteitsaanpak.

| | |
|---|---|
| Versie | 0.1 (concept) |
| Eigenaar | Kwaliteitsmanager GBO (in te vullen) |
| Reviewers | Software delivery manager, architect, vertegenwoordiger RINIS (in te vullen) |
| Gebaseerd op | ICTU Kwaliteitsaanpak v5.4.1 |

## 1. Scope

Dit plan geldt voor alle software die het programma GBO ontwikkelt:

- **Referentiecomponenten** die bronhouders zelf draaien, zoals de bronontsluiting (FSC/GraphQL/PBAC), de
  GBO-vertaallaag en het decentrale configuratiecomponent.
- **Centrale voorzieningen**, zoals de OOTS-adapter, de ASI-provider, de PubEAA-voorziening en de
  toestemmingsvoorziening.
- **Conformancetests** waarmee wordt aangetoond dat een implementatie aan de GBO-afspraken voldoet.

Omdat bronhouders referentiecomponenten in hun eigen omgeving gebruiken of er alternatieven voor bouwen, gelden
voor GBO aanvullende eisen aan herbruikbaarheid, versiebeheer en transparantie (zie §7).

## 2. Kwaliteitsnormen broncode

Quality-time bewaakt deze normen. SonarQube levert de metingen, met het standaard *Sonar way*-profiel.

| Norm | Waarde | Bron |
|---|---|---|
| Cyclomatische complexiteit per methode | ≤ 10; 0% van de methoden overschrijdt dit | ICTU-template kwaliteitsplan |
| Duplicatie | 0% (SonarQube, standaardinstellingen) | idem |
| Omvang per methode | ≤ 20 non-comment source statements; 0% overschrijdt dit | idem |
| Parameters per methode | ≤ 5; 0% overschrijdt dit | idem |
| Omvang per deelsysteem | Per deelsysteem vast te stellen in het SAD; waarschuwing bij 80% | idem |
| Unit-testdekking (regels) | ≥ 80% op nieuwe code (SonarQube quality gate) | GBO-keuze |
| Functionele testdekking | ≥ 80% van de logische testgevallen geautomatiseerd | DoD ICTU-template |
| Bekende kwetsbaarheden | Geen *critical* of *high* in dependencies en images zonder geaccepteerde uitzondering | GBO-keuze, M16 |
| Secrets in code | Nul (gitleaks) | ICTU review-checklist |
| Toegankelijkheid (componenten met UI) | Geen axe-overtredingen; WCAG 2.2 AA | M07, NFE-template |

**Uitzonderingen** op een norm worden vastgelegd als *technische schuld* in Quality-time, met reden en
geplande oplossing (M08). Een uitzondering op een kwetsbaarheid wordt vastgelegd in `.trivyignore` met
een verwijzing naar het issue en een vervaldatum.

### Codeerstandaarden

| Taal | Standaard | Controle |
|---|---|---|
| Go | Effective Go, `gofmt`, `golangci-lint` standaardset | pre-commit en CI |
| TypeScript/JavaScript | ESLint (recommended) en Prettier | pre-commit en CI |
| Python | PEP 8 via `ruff` | pre-commit en CI |
| Java | Google Java Style | CI |
| GraphQL-schema's | `graphql-schema-linter` | CI |

Pas deze tabel aan zodra de technologiekeuzes in het SAD vastliggen.

## 3. Ontwikkelproces

GBO werkt volgens Scrum (M05). Al het werk loopt via de product backlog.

### Definition of Ready

Een user story is *ready* als:

1. de story voldoet aan de INVEST-criteria;
2. acceptatiecriteria zijn beschreven;
3. relevante niet-functionele eisen en de betrokken GBO-afspraak of -standaard zijn benoemd;
4. bekend is welke logische testgevallen de story aantonen, of dat die tijdens de sprint worden opgesteld;
5. afhankelijkheden van andere partijen (bronhouders, RINIS, Logius) zijn bekend;
6. de story is besproken in de refinement en geschat.

### Definition of Done

Een user story is *done* als:

1. de code voldoet aan de codeerstandaard en door minstens één andere ontwikkelaar is gereviewd;
2. nieuwe en gewijzigde testgevallen zijn gereviewd;
3. alle geautomatiseerde tests in de pipeline slagen;
4. de SonarQube quality gate is groen;
5. er geen nieuwe kwetsbaarheden (critical/high) zijn zonder geaccepteerde uitzondering;
6. de story traceerbaar is: de PR verwijst naar de story, en de tests verwijzen naar de logische testgevallen;
7. relevante documentatie is bijgewerkt: README, API-schema, SAD of ADR bij een architectuurbeslissing,
   installatie- en beheerdocumentatie;
8. bij een wijziging van een koppelvlak de conformancetests zijn bijgewerkt;
9. bij componenten met een gebruikersinterface de toegankelijkheidstest slaagt;
10. de demo voor de sprint review is voorbereid.

Het PR-template (`templates/.github/pull_request_template.md`) bevat deze lijst. De pipeline controleert dat
elk item is afgevinkt of expliciet als *n.v.t.* is gemarkeerd.

### Broncodereviews

- Elke pull request wordt door minimaal één andere ontwikkelaar gereviewd voordat hij wordt gemerged.
- Gebruik de review-checklist uit het ICTU-template: functionaliteit, codekwaliteit, onderhoudbaarheid,
  veiligheid (geen secrets, inputvalidatie), performance, tests en documentatie.
- Wijzigingen aan autorisatie (PEP/PDP/policies), pseudonimisering, cryptografie of het verwerken van het BSN
  worden gereviewd door een tweede reviewer met securitykennis.

### Traceerbaarheid (M03)

- Elke pull request verwijst in titel of beschrijving naar een story of issue (bijvoorbeeld `GBO-123` of `#45`).
- Fysieke testgevallen dragen het ID van het logische testgeval, bijvoorbeeld in de testnaam of een annotatie
  (`// LTC: GBO-LTC-017`).
- Niet-functionele eisen worden gekoppeld aan tests of aan een handmatige verificatie in Quality-time.

### Versiebeheer

- `main` is beschermd: alleen via pull request, met geslaagde checks en een review.
- Branches leven kort en worden na de merge verwijderd.
- Commits volgen [Conventional Commits](https://www.conventionalcommits.org/nl/v1.0.0/); release notes worden
  daaruit gegenereerd.
- Releases krijgen een semantische versie (`vMAJOR.MINOR.PATCH`).

## 4. Testen

Het mastertestplan beschrijft welke testsoorten met welke intensiteit worden uitgevoerd. Dit plan legt vast
waar ze in de pipeline zitten.

| Testsoort | Moment | Werkwijze | Maatregel |
|---|---|---|---|
| Unit tests | Elke PR | Projectspecifiek; dekking naar SonarQube | M07 |
| Regressietests (geautomatiseerd) | Elke PR | Volledige set; dekking bewaakt in Quality-time | M04 |
| Contract- en conformancetests | Elke PR die een koppelvlak raakt; nachtelijk | Tegen GBO-afspraken (GraphQL, AuthZEN, LDV, FSC) | M03, M07 |
| Statische securityanalyse | Elke PR | SonarQube | M16 |
| Dependency- en imagescan | Elke PR en nachtelijk | Trivy; SBOM naar Dependency-Track | M16 |
| Dynamische securityscan | Na deploy op test; nachtelijk volledig | ZAP | M07, M16 |
| Toegankelijkheid | Na deploy op test (componenten met UI) | axe | M07 |
| Performance | Nachtelijk of per sprint | JMeter / Performancetestrunner | M07 |
| Penetratietest en code review door experts | Elke grote release, minimaal 2× per jaar | Extern, via ICTU | M26 |

## 5. Beheer van dependencies

Gebaseerd op de ICTU-aanbevelingen voor het beheer van dependencies (template kwaliteitsplan, bijlage E):

1. Dependabot opent wekelijks pull requests voor updates van alle dependencies, inclusief GitHub Actions en
   container-images.
2. Er geldt een cooldown van 14 dagen: nieuwe versies worden pas na 14 dagen voorgesteld, om het risico op
   supply chain attacks te beperken. Beveiligingsupdates zijn hiervan uitgezonderd.
3. Elke build levert een SBOM in CycloneDX-formaat; Dependency-Track bewaakt alle SBOM's continu op nieuwe
   kwetsbaarheden.
4. Versies worden vastgepind (lockfiles, image-digests). GitHub Actions van derden worden op commit-SHA
   vastgepind.

## 6. Kwaliteitsbewaking en rapportage

- Quality-time meet de normen continu (M02). Het team bekijkt dagelijks de afwijkingen; de kwaliteitsmanager
  bespreekt ze in de daily scrum of het projectoverleg.
- Technische schuld wordt gemarkeerd in Quality-time, geschat en planmatig opgelost: richtwaarde circa 10%
  van de sprintcapaciteit (M08).
- De projectleider organiseert periodiek een self-assessment tegen de Kwaliteitsaanpak (M28). Gebruik daarvoor
  de Quality-time-variant van de checklist (zie `quality-time/README.md`).
- Escalatie bij langdurig niet halen van normen: kwaliteitsmanager → software delivery manager → projectleider
  → hoofd ICTU Software Expertise (M02).

### Vrijgave

Bij elke major release levert het project informatie voor het vrijgaveadvies van de opdrachtgevende
organisatie: gerealiseerde eisen en hoe die getoetst zijn, openstaande bugs, afwijkingen in de
kwaliteitsrapportage met de risico's daarvan, overige risico's en het advies van ICTU. De release-workflow
levert release notes, SBOM en build-provenance automatisch.

## 7. Aanvullende eisen voor GBO

Deze eisen volgen uit de rol van GBO-software als herbruikbare referentie voor bronhouders.

1. **Conformance.** Voor elke GBO-afspraak met een koppelvlak bestaat een conformance-testsuite die zowel op de
   referentiecomponent als op een alternatieve implementatie van een bronhouder kan draaien.
2. **Open source.** Referentiecomponenten zijn openbaar, met een licentie, README, installatie- en
   configuratiedocumentatie. De [Standard for Public Code](https://standard.publiccode.net/) dient als checklist.
3. **Releases.** Releases zijn ondertekend of voorzien van build-provenance, met SBOM en release notes.
   Breaking changes in een koppelvlak worden vooraf aangekondigd.
4. **Gescheiden omgevingen en testdata.** Ontwikkel-, test- en productieomgevingen zijn gescheiden. Testen
   gebruiken alleen synthetische testdata; nooit echte BSN's of persoonsgegevens.
5. **Logging en verantwoording.** Componenten die gegevens verwerken loggen volgens de LDV-standaard en, voor
   autorisatiebeslissingen, de Authorization Decision Log. Logging bevat geen BSN's in leesbare vorm.

## 8. AI-ondersteund ontwikkelen

De Kwaliteitsaanpak zegt (nog) niets over AI-assistenten. Voor GBO gelden voorlopig deze afspraken, af te
stemmen met ICTU en RINIS:

1. De ontwikkelaar die een wijziging indient blijft verantwoordelijk voor de inhoud, ook als een
   AI-assistent de code of tekst heeft opgesteld.
2. AI-gegenereerde wijzigingen doorlopen dezelfde pipeline en dezelfde menselijke review als ander werk.
3. Geef AI-assistenten geen secrets, credentials, productiegegevens of persoonsgegevens.
4. De Claude Code-skill en hooks uit deze repository mogen gebruikt worden, maar zijn nooit de enige controle:
   de pipeline is leidend.

## Open punten

| # | Punt | Eigenaar | Status |
|---|---|---|---|
| 1 | Kwaliteits- en beveiligingseisen van RINIS ontvangen en verwerken (verwacht: ISO 27001 Annex A 8.25-8.33) | Programma GBO | Opgevraagd |
| 2 | Licentie kiezen: EUPL-1.2 gekozen | Programma GBO | Afgerond |
| 3 | Instanties van SonarQube, Quality-time en Dependency-Track afspreken met ICTU ISD (M29) | Projectleider | Open |
| 4 | Afspraken over AI-ondersteund ontwikkelen bevestigen met ICTU en RINIS | Kwaliteitsmanager | Open |
| 5 | Technologiekeuzes vastleggen in het SAD en de codeerstandaarden hierop aanpassen | Architect | Open |
| 6 | Mastertestplan opstellen, inclusief productrisicoanalyse | Opdrachtgevende organisatie | Open |
