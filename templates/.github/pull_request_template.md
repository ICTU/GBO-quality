## Wat en waarom

<!-- Korte beschrijving van de wijziging en de aanleiding. -->

Story/issue: <!-- bijv. GBO-123 of Closes #45 (verplicht, ICTU-maatregel M03) -->

## Hoe getest

<!-- Welke tests zijn toegevoegd of aangepast? Noem de ID's van de logische testgevallen. -->

## Definition of Done

<!--
Vink elk item af. Is een item niet van toepassing, laat het open en zet erachter
"n.v.t.: <reden>". De pipeline controleert deze lijst.
-->

<!-- dod:start -->
- [ ] Code voldoet aan de codeerstandaard en is door een andere ontwikkelaar gereviewd
- [ ] Nieuwe en gewijzigde testgevallen zijn gereviewd
- [ ] Tests verwijzen naar de logische testgevallen (traceerbaarheid)
- [ ] Alle pipeline-checks slagen, inclusief SonarQube quality gate en kwetsbaarhedenscan
- [ ] Documentatie is bijgewerkt (README, API-schema, installatie- en beheerdocumentatie)
- [ ] Architectuurbeslissing vastgelegd in een ADR en het SAD bijgewerkt
- [ ] Conformancetests bijgewerkt bij een wijziging van een koppelvlak
- [ ] Toegankelijkheidstest slaagt bij een wijziging van de gebruikersinterface
- [ ] Geen secrets, echte persoonsgegevens of BSN's in code, tests of logging
- [ ] Demo voor de sprint review is voorbereid
<!-- dod:end -->

## Aandachtspunten voor de reviewer

<!-- Risico's, keuzes of plekken waar je extra kritisch naar wilt laten kijken.
Raakt de wijziging autorisatie, pseudonimisering, cryptografie of BSN-verwerking?
Vraag dan een tweede reviewer met securitykennis. -->
