# Een GBO-repository aansluiten

Stappenplan om een nieuwe of bestaande GBO-repository aan te sluiten op de centrale kwaliteitsafspraken.

## 1. Templates kopiëren

```bash
./GBO-quality/scripts/aansluiten.sh pad/naar/repository
```

Het script kopieert alleen bestanden die nog niet bestaan; bestaande bestanden worden niet overschreven.
Het kopieert:

- `.github/workflows/ci.yml`: roept de centrale workflows aan;
- `.github/workflows/release.yml`: release met testrapport en bewijsbundel;
- `.github/workflows/periodiek.yml` en `.github/kwaliteitskalender.yml`: kwaliteitskalender en wekelijkse
  controles van kwetsbaarheden en toegang;
- `docs/rollback.md` en `docs/testgevallen/`: sjablonen voor de rollbackinstructie en de logische
  testgevallen;
- `.github/pull_request_template.md`: met de Definition of Done;
- `.github/dependabot.yml`: wekelijkse updates met cooldown;
- `.github/CODEOWNERS`;
- `.pre-commit-config.yaml`;
- `sonar-project.properties` en `cliff.toml`;
- `SECURITY.md`: meldpunt voor kwetsbaarheden (kwaliteitsplan §8.4);
- `AGENTS.md`: instructies voor alle AI-codeerassistenten (Claude Code, Codex, Copilot en andere);
- `CLAUDE.md` en `.claude/`: importeert AGENTS.md, plus skill en hooks voor Claude Code.

## 2. Aanpassen aan de component

- `ci.yml`: vul het testcommando en de taal in, en pas `dod-regels` aan op de mappen van de component.
  Daarmee vervallen DoD-items over koppelvlakken, gebruikersinterface en risicoanalyse automatisch
  als een PR die paden niet raakt.
- `sonar-project.properties`: projectsleutel en bronmappen.
- `.pre-commit-config.yaml`: zet de linters aan voor de gebruikte taal.
- `CODEOWNERS`: teams of personen.
- `SECURITY.md`: ondersteunde versies en contactpersoon; zet *Private vulnerability reporting* aan
  (Settings → Code security).
- `AGENTS.md`: korte beschrijving van de component en hoe je lokaal test. Zet gedeelde AI-instructies
  hier, niet in `CLAUDE.md`.
- `release.yml`: vul `test-command` in, zodat de tests op de getagde versie draaien en JUnit-XML
  opleveren voor het testrapport. Schrijf de rollbackinstructie in `docs/rollback.md` en leg de
  logische testgevallen vast in `docs/testgevallen/`.
- `.github/kwaliteitskalender.yml`: vul de beheerders, de eigenaren van de taken en de startmaanden in.
- `periodiek.yml`: vul `image-ref` in als de component een container-image publiceert.

## 3. Secrets en variabelen instellen

Op repository- of organisatieniveau (Settings → Secrets and variables → Actions):

| Naam | Soort | Nodig voor |
|---|---|---|
| `SONAR_TOKEN` | Secret | SonarQube-analyse |
| `SONAR_HOST_URL` | Variabele | SonarQube-analyse |
| `DT_API_KEY` | Secret | SBOM-upload naar Dependency-Track |
| `DT_URL` | Variabele | idem |
| `GBO_AUDIT_TOKEN` | Secret (optioneel) | Toegangscontrole: MFA in de organisatie en beheerders van de repository |

Het audittoken is een fine-grained token of GitHub App met alleen leesrechten: *Members* en
*Administration* (organisatie) en *Administration* en *Metadata* (repository). Zonder dit token
controleert de toegangscontrole alleen de bescherming van `main`. De controle op leden zonder MFA werkt
alleen met een token van een organisatie-eigenaar.

Ontbreekt een secret, dan slaat de betreffende stap over met een waarschuwing. Zo kun je beginnen voordat
alle tooling beschikbaar is. Zet zodra de tooling er is de bijbehorende input `require-...: true`, zodat
een ontbrekende configuratie de build laat falen.

## 4. Branch protection voor `main`

Settings → Rules → Rulesets, of Branches → Branch protection rules:

- Require a pull request before merging, met minimaal 1 approval.
- Require review from Code Owners.
- Dismiss stale approvals when new commits are pushed.
- Require status checks to pass: `quality / ci`, `pr / traceerbaarheid`, `pr / definition-of-done`.
- Require linear history (squash merge).
- Block force pushes.

Gebruik bij voorkeur een ruleset: de wekelijkse toegangscontrole kan de instellingen daarvan lezen en
meldt het als er iets ontbreekt.

Zet daarnaast aan:

- Settings → General → Releases: **immutable releases**, zodat een release met testrapport en
  bewijsbundel na publicatie niet meer te wijzigen is (kwaliteitsplan §6 en §8.1);
- Settings → General → Pull Requests: **automatically delete head branches**.

Controleer ook dat de GitHub-organisatie tweestapsverificatie (MFA) verplicht stelt en dat beheerrechten
bij een kleine, benoemde groep liggen (kwaliteitsplan §8.5).

## 5. Quality-time

Voeg de repository toe aan het GBO-rapport in Quality-time. Zie `quality-time/README.md`.

## 6. Lokaal

```bash
pip install pre-commit   # of: brew install pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg
```
