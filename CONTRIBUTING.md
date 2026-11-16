# Bijdragen aan GBO-quality

Dank voor je interesse in het bijdragen aan GBO-quality!

## Gedragscode

Door bij te dragen ga je akkoord met de [gedragscode](CODE_OF_CONDUCT.md),
gebaseerd op de [Contributor Covenant](https://www.contributor-covenant.org/).

## Werkwijze

1. Maak een [issue](https://github.com/ICTU/GBO-quality/issues) aan met de voorgestelde wijziging en de
   reden ervoor.
2. Werk op een branch (of in een fork als je geen schrijfrechten hebt):
   `git checkout -b feature/mijn-wijziging`
3. Open een pull request naar `main` die naar het issue verwijst (`Closes #12`) en vul de Definition of Done
   in het PR-template in.
4. Wijzigingen in `docs/kwaliteitsplan.md` (normen, Definition of Done) vereisen goedkeuring van de
   kwaliteitsmanager. Dit is vastgelegd in `.github/CODEOWNERS`.
5. Wijzigingen in de herbruikbare workflows test je eerst in één GBO-repository door naar je branch te
   verwijzen (`@mijn-branch`) voordat je merget.

Lokaal controleren: zie [AGENTS.md](AGENTS.md) voor de test-, lint- en pre-commit-commando's.

## Commitberichten

We gebruiken [Conventional Commits](https://www.conventionalcommits.org/nl/v1.0.0/):
`feat:`, `fix:`, `docs:`, `ci:`, `chore:`, `refactor:`, `test:`. Release notes worden hieruit gegenereerd.

## GitHub Actions

Pin elke action van derden op een volledige commit-SHA (niet op een tag of branch), met de versie als
commentaar, conform de [ICTU GitHub policy](https://github.com/ICTU/github-policy). Kies bij updates een
release die minstens 14 dagen oud is.

## Releases

Na merge naar `main` met een gebruikersrelevante wijziging:

```bash
git tag v0.2.0 && git push origin v0.2.0
git tag -f v0 && git push -f origin v0   # verplaats de major-tag
```

Een breaking change (bijvoorbeeld een nieuw verplicht input in een workflow) krijgt een nieuwe major-tag.
Werk [CHANGELOG.md](CHANGELOG.md) bij.

## Hulp nodig?

Neem contact op met de repository-eigenaar (zie [README.md](README.md#contact)).
