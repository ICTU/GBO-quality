# Een GBO-repository aansluiten

Stappenplan om een nieuwe of bestaande GBO-repository aan te sluiten op de centrale kwaliteitsafspraken.

## 1. Templates kopiëren

```bash
./GBO-quality/scripts/aansluiten.sh pad/naar/repository
```

Het script kopieert alleen bestanden die nog niet bestaan; bestaande bestanden worden niet overschreven.
Het kopieert:

- `.github/workflows/ci.yml`: roept de centrale workflows aan;
- `.github/pull_request_template.md`: met de Definition of Done;
- `.github/dependabot.yml`: wekelijkse updates met cooldown;
- `.github/CODEOWNERS`;
- `.pre-commit-config.yaml`;
- `sonar-project.properties` en `cliff.toml`;
- `CLAUDE.md` en `.claude/`: skill en hooks voor Claude Code.

## 2. Aanpassen aan de component

- `ci.yml`: vul het testcommando en de taal in.
- `sonar-project.properties`: projectsleutel en bronmappen.
- `.pre-commit-config.yaml`: zet de linters aan voor de gebruikte taal.
- `CODEOWNERS`: teams of personen.
- `CLAUDE.md`: korte beschrijving van de component en hoe je lokaal test.

## 3. Secrets en variabelen instellen

Op repository- of organisatieniveau (Settings → Secrets and variables → Actions):

| Naam | Soort | Nodig voor |
|---|---|---|
| `SONAR_TOKEN` | Secret | SonarQube-analyse |
| `SONAR_HOST_URL` | Variabele | SonarQube-analyse |
| `DT_API_KEY` | Secret | SBOM-upload naar Dependency-Track |
| `DT_URL` | Variabele | idem |

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

## 5. Quality-time

Voeg de repository toe aan het GBO-rapport in Quality-time. Zie `quality-time/README.md`.

## 6. Lokaal

```bash
pip install pre-commit   # of: brew install pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg
```
