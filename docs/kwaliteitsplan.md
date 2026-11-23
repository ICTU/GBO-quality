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
| Gebaseerd op | ICTU Kwaliteitsaanpak v5.4.1; BIO2 v1.3; NEN-EN-ISO/IEC 27001:2023 en 27002:2022 (zie §8) |

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
| Hersteltermijn kwetsbaarheden in uitgebrachte versies | Hoge kans op misbruik én hoge schade: patchrelease of mitigatieadvies binnen 1 week (zie §8.4) | BIO2 v1.3, 8.08.01 |
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
3. relevante niet-functionele eisen en de betrokken GBO-afspraak of -standaard zijn benoemd, inclusief de
   beveiligingseisen; bij een significante wijziging is de risicoanalyse van de component bijgewerkt
   (zie §8.2);
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
10. de demo voor de sprint review is voorbereid;
11. bij een significante wijziging de risicoanalyse van de component is bijgewerkt (zie §8.2) (bron: BIO2
    v1.3, 5.08.01).

Voldoen aan de kwaliteitsnormen is onderdeel van de Definition of Done (bron: ICTU Kwaliteitsaanpak
v5.4.1, M02). Om de ontwikkelaar niet te belasten met afvinken van wat al vaststaat, is de borging per
item verdeeld:

| Item | Borging |
|---|---|
| 1, 3, 4, 5 | Pipeline en branch protection: pre-commit en linters, verplichte review, verplichte status checks (SonarQube, Trivy) |
| 2 | Onderdeel van de verplichte review van de pull request |
| 6 | Story-ID: traceerbaarheidscheck in de pipeline; verwijzing naar logische testgevallen: DoD-item in de PR |
| 7 | DoD-item in de PR |
| 8, 9, 11 | Voorwaardelijk DoD-item in de PR: vervalt automatisch als de PR de bijbehorende paden niet raakt |
| 10 | Sprint review, niet per pull request |

Het PR-template (`templates/.github/pull_request_template.md`) bevat alleen de items die een mens moet
beoordelen. De pipeline controleert dat elk item is afgevinkt of expliciet als *n.v.t.* is gemarkeerd.
Een voorwaardelijk item draagt een sleutel (`<!-- dod:koppelvlak -->`); de input `dod-regels` van de
workflow koppelt die sleutel aan paden in de repository. Raakt de PR geen van die paden, dan is het
item niet van toepassing zonder dat de ontwikkelaar iets hoeft te doen.

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
| Penetratietest en code review door experts | Elke grote release, minimaal 2× per jaar; voor internetfacing componenten bij elke nieuwe release of major update (zie §8.4) | Extern, via ICTU; waar mogelijk geautomatiseerd | M26, BIO2 8.08.05 |

Van elke release wordt een testrapport gemaakt: welke tests zijn uitgevoerd, met welk resultaat, en welke
bevindingen openstaan. De release-workflow maakt dit rapport automatisch (zie §6, *Vrijgave en bewijs per
release*). Het mastertestplan beschrijft de gestructureerde testmethode (bron: BIO2 v1.3,
8.29.01; NEN-EN-ISO/IEC 27002:2022, 8.29).

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
5. Dependency-Track bewaakt ook de licenties van dependencies; een licentie die niet verenigbaar is met
   EUPL-1.2 is een bevinding die vóór de volgende release is opgelost (bron: NEN-EN-ISO/IEC 27002:2022, 5.32 en 8.28).
6. Dependencies die *end-of-life* zijn of niet meer worden onderhouden, worden als technische schuld
   gemarkeerd en vervangen. Kies bij voorkeur gangbare, goed onderhouden componenten, zeker voor
   authenticatie en cryptografie (bron: NEN-EN-ISO/IEC 27002:2022, 5.21 en 8.28).

## 6. Kwaliteitsbewaking en rapportage

- Quality-time meet de normen continu (M02). Het team bekijkt dagelijks de afwijkingen; de kwaliteitsmanager
  bespreekt ze in de daily scrum of het projectoverleg.
- Technische schuld wordt gemarkeerd in Quality-time, geschat en planmatig opgelost: richtwaarde circa 10%
  van de sprintcapaciteit (M08).
- De projectleider organiseert periodiek een self-assessment tegen de Kwaliteitsaanpak (M28); zie de
  kwaliteitskalender hieronder.
- Escalatie bij langdurig niet halen van normen: kwaliteitsmanager → software delivery manager → projectleider
  → hoofd ICTU Software Expertise (M02).

### Kwaliteitskalender en periodieke controles

Periodieke activiteiten staan in de kwaliteitskalender (`.github/kwaliteitskalender.yml` in de
componentrepository). Een wekelijkse workflow maakt aan het begin van elke periode een issue met checklist,
bron en deadline. Het issue sluiten, met het bewijs erbij, is de vastlegging. Een open issue na de
deadline krijgt het label `te-laat`, zodat Quality-time het kan meten.

| Activiteit | Frequentie | Bron |
|---|---|---|
| Penetratietest en code review door experts | Halfjaarlijks; internetfacing componenten ook bij elke release | ICTU Kwaliteitsaanpak v5.4.1, M26; BIO2 v1.3, 8.08.05; §4 en §8.4 |
| Self-assessment tegen de Kwaliteitsaanpak | Halfjaarlijks (GBO-keuze; M28 zegt "periodiek") | ICTU Kwaliteitsaanpak v5.4.1, M28 |
| Toegangsrechten op repository en tooling bevestigen | Per kwartaal (GBO-keuze) | BIO2 v1.3, 5.17.01; NEN-EN-ISO/IEC 27002:2022, 5.18; §8.5 |
| Register van clouddiensten en tools herzien | Jaarlijks (GBO-keuze) | NEN-EN-ISO/IEC 27002:2022, 5.23; BIO2 v1.3, 5.23.01; §8.6 |
| Training of workshop veilig programmeren | Jaarlijks | NEN-EN-ISO/IEC 27001:2023, 7.2; §8.9 |
| Risicoanalyses nalopen op actualiteit | Jaarlijks (GBO-keuze), naast herhaling bij significante wijziging | BIO2 v1.3, 5.08.01; §8.2 |

Naast de kalender controleert dezelfde workflow wekelijks automatisch:

- **Kwetsbaarheden:** de Trivy-scan maakt per kwetsbaarheid met ernst critical of high een issue met een
  deadline van 7 dagen en een checklist voor de risicoafweging; de afweging kan een andere termijn
  vastleggen. Het issue wordt heropend als de kwetsbaarheid terugkomt (bijvoorbeeld na het verlopen van een
  uitzondering) en gesloten als de scan hem niet meer vindt (bron: BIO2 v1.3, 8.08.01-8.08.03; §8.4).
  Uitzonderingen in `.trivyignore` hebben een vervaldatum (`exp:JJJJ-MM-DD`).
- **Toegang:** of de organisatie MFA verplicht stelt, welke leden geen MFA hebben, of alleen de benoemde
  beheerders beheerrechten hebben en of `main` beschermd is. Het rapport staat bij elke run; een afwijking
  wordt een issue dat vanzelf sluit als alles weer klopt (bron: BIO2 v1.3, 5.17.01;
  NEN-EN-ISO/IEC 27002:2022, 8.2 en 8.4; §8.5).

### Vrijgave en bewijs per release

Bij elke major release levert het project informatie voor het vrijgaveadvies van de opdrachtgevende
organisatie: gerealiseerde eisen en hoe die getoetst zijn, openstaande bugs, afwijkingen in de
kwaliteitsrapportage met de risico's daarvan, overige risico's en het advies van ICTU.

De release-workflow levert dit grotendeels automatisch, bij elke release:

- release notes uit Conventional Commits, met de rollbackinstructie (§8.8);
- het testrapport (§4): resultaten van de geautomatiseerde tests op de getagde versie, traceerbaarheid en
  dekking van de logische testgevallen, kwetsbaarheden en geaccepteerde uitzonderingen, gemergde pull
  requests met hun reviewers, openstaande bugs en een samenvatting van de aandachtspunten;
- een bewijsbundel (`bewijs-<versie>.zip`) met het testrapport, de onderliggende testresultaten en scans,
  de SBOM, de gegevens over pull requests en reviews, herkomstgegevens en een SHA-256-manifest;
- build-provenance voor SBOM, testrapport, bewijsbundel en artefacten.

Falen de tests op de getagde versie, dan maakt de workflow geen release. De repository gebruikt *immutable
releases*, zodat een release met zijn bijlagen na publicatie niet meer te wijzigen is. Zo blijft het bewijs
beschikbaar en beschermd tegen wijziging, en is het bij afsluiting of overdracht direct te archiveren
(bron: NEN-EN-ISO/IEC 27001:2023, 7.5.3; ICTU Kwaliteitsaanpak v5.4.1, M27 en M34). Resultaten van tests
buiten de pipeline, zoals pentests, worden vastgelegd in het betreffende kalender-issue.

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
   Zie ook §8.7.
6. **Pseudonimisering.** Waar een component pseudonimiseert, tonen tests aan dat de pseudoniemen niet
   zonder sleutel tot de persoon te herleiden zijn, ook niet via combinatie met andere velden in dezelfde
   uitvoer (bron: NEN-EN-ISO/IEC 27002:2022, 8.11).

## 8. Informatiebeveiliging

Voor de overheid is de BIO verplicht. De BIO eist een managementsysteem voor informatiebeveiliging (ISMS)
volgens NEN-EN-ISO/IEC 27001 en beheersmaatregelen volgens NEN-EN-ISO/IEC 27002, aangevuld met
verplichte overheidsmaatregelen (bron: BIO2 v1.3, deel 1 §3 en §4). De ICTU Kwaliteitsaanpak noemt de BIO
als bron voor niet-functionele eisen (bron: ICTU Kwaliteitsaanpak v5.4.1, Beschrijving van niet-functionele
eisen). Deze paragraaf legt vast hoe GBO-software daaraan bijdraagt.

### 8.1 Rol van dit plan

- Het ISMS, de risicobeoordeling en de Verklaring van toepasselijkheid (VvT) zijn van de organisatie die
  verantwoordelijk is voor de dienstverlening: RINIS, de opdrachtgever of de bronhouder. Dit plan is geen
  ISMS (bron: NEN-EN-ISO/IEC 27001:2023, 4.3, 6.1.3; BIO2 v1.3, deel 1 §5 en §7).
- Voor die organisatie is GBO een leverancier van software. Zij moet extern geleverde producten beheersen
  en blijft verantwoordelijk voor de risico's daarvan (bron: NEN-EN-ISO/IEC 27001:2023, 8.1; BIO2 v1.3,
  deel 1 §13). Dit plan beschrijft daarom de **opzet** van de maatregelen in de ontwikkeling; de pipeline,
  Quality-time, testrapporten en pentestrapporten leveren het bewijs van **bestaan** en **werking**
  (bron: BIO2 v1.3, deel 1 §4).
- Bewijs (scanresultaten, reviews, testrapporten, pentestrapporten, release-artefacten) blijft beschikbaar,
  is beschermd tegen wijziging en wordt bij afsluiting of overdracht gearchiveerd (bron:
  NEN-EN-ISO/IEC 27001:2023, 7.5.3; ICTU Kwaliteitsaanpak v5.4.1, M27 en M34).
- [maatregelen-mapping.md](maatregelen-mapping.md) laat per beheersmaatregel zien hoe GBO hem invult. Gebruik
  die tabel als bijdrage aan de VvT van de verantwoordelijke organisatie.

### 8.2 Risicoanalyse en beveiligingseisen

- Elke component heeft een vastgelegde risicoanalyse: welke gegevens hij verwerkt, de BIV-classificatie
  (beschikbaarheid, integriteit, vertrouwelijkheid), een dreigingsmodel en de beveiligingseisen die daaruit
  volgen. GBO gebruikt daarvoor de methode Grip op SSD, die de Kwaliteitsaanpak noemt (bron: BIO2 v1.3,
  5.08.01; NEN-EN-ISO/IEC 27002:2022, 5.8 en 8.26; ICTU Kwaliteitsaanpak v5.4.1, Beschrijving van
  niet-functionele eisen).
- De analyse wordt herhaald bij een significante wijziging, zoals een nieuw koppelvlak, een nieuw soort
  gegevens of een nieuwe hostingomgeving (bron: BIO2 v1.3, 5.08.01; NEN-EN-ISO/IEC 27001:2023, 8.2).
- Beveiligingseisen worden net als andere eisen vertaald naar logische testgevallen (zie §3,
  traceerbaarheid) (bron: NEN-EN-ISO/IEC 27002:2022, 8.29).
- Informatiebeveiligingsrisico's van het project zelf staan in de risicolog (bron: ICTU Kwaliteitsaanpak
  v5.4.1, M30; NEN-EN-ISO/IEC 27002:2022, 5.8).

### 8.3 Architectuurprincipes

Het SAD legt per component vast hoe deze principes zijn toegepast; afwijkingen worden in een ADR
verantwoord (bron: BIO2 v1.3, 8.27.01; NEN-EN-ISO/IEC 27002:2022, 8.27):

- *security by design* en *security by default*: veilige standaardconfiguratie, onveilige opties
  uitgeschakeld;
- *zero trust*: elk verzoek wordt geauthenticeerd en geautoriseerd, ook binnen het netwerk (FSC, PEP/PDP);
- *least privilege* en *least functionality*: alleen de rechten, endpoints en functies die nodig zijn;
- *fail securely* en *default deny*: bij twijfel of fouten wordt toegang geweigerd;
- *distrust input*: alle invoer van buiten de component wordt gevalideerd;
- *defence in depth*: uitval van één maatregel leidt niet direct tot een kwetsbaarheid (bron: BIO2 v1.3,
  deel 1 §4).

### 8.4 Kwetsbaarhedenbeheer

- Elke componentrepository heeft een `SECURITY.md` met een meldpunt voor kwetsbaarheden (GitHub Private
  Vulnerability Reporting) (bron: NEN-EN-ISO/IEC 27002:2022, 8.8).
- Dependency-Track en de nachtelijke Trivy-scan signaleren nieuwe kwetsbaarheden in uitgebrachte versies.
  Is zowel de kans op misbruik als de verwachte schade hoog, dan levert GBO binnen een week een patchrelease
  of een mitigatieadvies aan de beheerders en bronhouders. Bij andere kwetsbaarheden bepaalt een
  vastgelegde risicoafweging de termijn (bron: BIO2 v1.3, 8.08.01-8.08.03).
- Internetfacing componenten (zoals de OOTS-adapter en de PubEAA-voorziening) krijgen bij elke nieuwe
  release of major update een penetratietest, waar mogelijk geautomatiseerd. Een bevinding met hoog risico
  die niet anders te mitigeren is, blokkeert de release voor productie. Daarnaast worden ze minimaal
  jaarlijks getest (bron: BIO2 v1.3, 8.08.04-8.08.05; ICTU Kwaliteitsaanpak v5.4.1, M26).
- Pentests en andere beveiligingstests op een productieomgeving gebeuren alleen na afspraak over scope,
  moment en toegang met de beheerder (bron: NEN-EN-ISO/IEC 27002:2022, 8.34).

### 8.5 Toegang tot broncode en tooling

- Multi-factorauthenticatie is verplicht voor alle accounts in de GitHub-organisatie en voor de
  ontwikkeltooling (SonarQube, Dependency-Track, Quality-time) (bron: BIO2 v1.3, 5.17.01).
- Schrijfrechten op repositories zijn beperkt tot het team; beheerrechten tot een kleine, benoemde groep.
  Wijzigingen komen alleen via een pull request in `main` (zie §3, versiebeheer) (bron:
  NEN-EN-ISO/IEC 27002:2022, 8.4 en 8.2).
- Secrets voor de pipeline staan in GitHub Secrets of een secretsmanager, nooit in code of configuratie in
  de repository (bron: NEN-EN-ISO/IEC 27002:2022, 8.24 en 8.28).

### 8.6 Leveranciersketen en clouddiensten

- GBO houdt een register bij van de gebruikte clouddiensten en externe tools (bijvoorbeeld GitHub,
  SonarQube, Dependency-Track en AI-assistenten): wat ze doen, welke gegevens ze krijgen, wie ervoor
  verantwoordelijk is, welke maatregelen bij de leverancier liggen en hoe GBO kan overstappen (bron:
  NEN-EN-ISO/IEC 27002:2022, 5.23; BIO2 v1.3, 5.23.01).
- Als leverancier aan bronhouders en beheerders levert GBO bij elke release een SBOM, build-provenance en
  documentatie over de beveiligingsfuncties en de veilige configuratie van de component (bron:
  NEN-EN-ISO/IEC 27002:2022, 5.21; BIO2 v1.3, 5.21.02-5.21.05).
- Wordt ontwikkeling uitbesteed, of bouwt een bronhouder een eigen alternatief, dan gelden dezelfde
  ontwikkelafspraken; de conformancetests en de eisen uit dit plan zijn de toets (bron: BIO2 v1.3,
  8.30.01; NEN-EN-ISO/IEC 27002:2022, 8.30).

### 8.7 Logging en cryptografie

- Een logregel van een component bevat minimaal actie, object, resultaat, oorsprong, actor en tijdstempel,
  en nooit gegevens die de beveiliging kunnen doorbreken, zoals wachtwoorden, tokens of sleutels (bron:
  BIO2 v1.3, 8.15.01-8.15.02; NEN-EN-ISO/IEC 27002:2022, 8.15).
- De documentatie van een component beschrijft welke logbestanden hij maakt, zodat de beheerder bewaartermijn
  en monitoring kan inrichten (bron: BIO2 v1.3, 8.15.03-8.15.04).
- Cryptografie volgt de actuele adviezen van het NCSC (zoals de ICT-beveiligingsrichtlijnen voor TLS) en de
  standaarden van het Forum Standaardisatie, via bewezen bibliotheken. Sleutels en certificaten zijn
  configureerbaar en staan nooit in de broncode (bron: BIO2 v1.3, 8.24.01 en 8.24.04;
  NEN-EN-ISO/IEC 27002:2022, 8.24).

### 8.8 Overdracht naar beheer

Wijzigingsbeheer in productie is de verantwoordelijkheid van de beheerorganisatie, volgens een algemeen
geaccepteerd beheerraamwerk (bron: BIO2 v1.3, 8.32.02). GBO levert daarvoor bij elke release:

- release notes met de wijzigingen en de impact, inclusief breaking changes (zie §7);
- het testrapport (zie §4);
- een rollbackinstructie;
- de bijgewerkte installatie- en beheerdocumentatie.

Zo kan de beheerder de risicoafweging en goedkeuring van de wijziging vastleggen (bron: BIO2 v1.3, 8.32.01;
NEN-EN-ISO/IEC 27002:2022, 8.32 en 5.37). GBO test niet in productieomgevingen; een uitzondering vraagt
vooraf goedkeuring van de proceseigenaar (bron: BIO2 v1.3, 8.31.01-8.31.02).

### 8.9 Kennis

Ontwikkelaars kennen de veelvoorkomende kwetsbaarheden (zoals de OWASP Top 10) en de afspraken in dit
plan. Nieuwe teamleden krijgen dit bij de onboarding; het team volgt jaarlijks een training of workshop
veilig programmeren en legt die deelname vast (bron: NEN-EN-ISO/IEC 27001:2023, 7.2;
NEN-EN-ISO/IEC 27002:2022, 8.25 en 8.28; ICTU Kwaliteitsaanpak v5.4.1, M23).

## 9. AI-ondersteund ontwikkelen

De Kwaliteitsaanpak zegt (nog) niets over AI-assistenten. Voor GBO gelden voorlopig deze afspraken, af te
stemmen met ICTU en RINIS:

1. De ontwikkelaar die een wijziging indient blijft verantwoordelijk voor de inhoud, ook als een
   AI-assistent de code of tekst heeft opgesteld.
2. AI-gegenereerde wijzigingen doorlopen dezelfde pipeline en dezelfde menselijke review als ander werk.
3. Geef AI-assistenten geen secrets, credentials, productiegegevens of persoonsgegevens.
4. De Claude Code-skill en hooks uit deze repository mogen gebruikt worden, maar zijn nooit de enige controle:
   de pipeline is leidend.
5. AI-assistenten zijn clouddiensten: ze staan in het register uit §8.6, met de gegevens die ze krijgen en
   de voorwaarden van de leverancier (bron: NEN-EN-ISO/IEC 27002:2022, 5.23).

## Open punten

| # | Punt | Eigenaar | Status |
|---|---|---|---|
| 1 | Kwaliteits- en beveiligingseisen van RINIS ontvangen en verwerken (verwacht: NEN-EN-ISO/IEC 27001:2023 Annex A 5.8, 8.4, 8.8, 8.9 en 8.25-8.34, met de BIO2-overheidsmaatregelen; §8 is de voorlopige invulling) | Programma GBO | Opgevraagd |
| 2 | Licentie kiezen: EUPL-1.2 gekozen | Programma GBO | Afgerond |
| 3 | Instanties van SonarQube, Quality-time en Dependency-Track afspreken met ICTU ISD (M29) | Projectleider | Open |
| 4 | Afspraken over AI-ondersteund ontwikkelen bevestigen met ICTU en RINIS | Kwaliteitsmanager | Open |
| 5 | Technologiekeuzes vastleggen in het SAD en de codeerstandaarden hierop aanpassen | Architect | Open |
| 6 | Mastertestplan opstellen, inclusief productrisicoanalyse | Opdrachtgevende organisatie | Open |
| 7 | Vaststellen welke organisatie per component het ISMS en de VvT beheert, en hoe GBO daaraan rapporteert (§8.1) | Programma GBO | Open |
| 8 | Risicoanalyse met Grip op SSD per component uitvoeren en vastleggen (§8.2) | Architect | Open |
| 9 | MFA afdwingen in de GitHub-organisatie en de ontwikkeltooling controleren (§8.5) | Software delivery manager | Open |
| 10 | Register van clouddiensten en externe tools opstellen, inclusief AI-assistenten (§8.6) | Kwaliteitsmanager | Open |
| 11 | Jaarlijkse training veilig programmeren inplannen (§8.9) | Projectleider | Open |
