## Wat en waarom

<!-- Korte beschrijving van de wijziging en de aanleiding. -->

Story/issue: <!-- bijv. GBO-123 of Closes #45 (verplicht, ICTU-maatregel M03) -->

## Hoe getest

<!-- Welke tests zijn toegevoegd of aangepast? Noem de ID's van de logische testgevallen. -->

## Definition of Done

<!--
Hier staan alleen de punten die een mens moet beoordelen. Codeerstandaard, review, slagende tests,
SonarQube en de kwetsbaarhedenscan borgen de pipeline en de branch protection; de demo hoort bij de
sprint review.

Vink elk item af. Is een item niet van toepassing, laat het open en zet erachter "n.v.t.: <reden>".
Items met een markering <!- - dod:... - -> vervallen vanzelf als de PR de bijbehorende paden niet raakt
(zie dod-regels in .github/workflows/ci.yml). De pipeline controleert deze lijst.
-->

<!-- dod:start -->
- [ ] Tests verwijzen naar de logische testgevallen (traceerbaarheid)
- [ ] Documentatie is bijgewerkt (README, API-schema, installatie- en beheerdocumentatie)
- [ ] Architectuurbeslissing vastgelegd in een ADR en het SAD bijgewerkt
- [ ] Geen secrets, echte persoonsgegevens of BSN's in code, tests of logging
- [ ] Conformancetests bijgewerkt bij een wijziging van een koppelvlak <!-- dod:koppelvlak -->
- [ ] Toegankelijkheidstest slaagt bij een wijziging van de gebruikersinterface <!-- dod:ui -->
- [ ] Risicoanalyse bijgewerkt bij een significante wijziging (nieuw koppelvlak, nieuw soort gegevens, nieuwe hosting) <!-- dod:risico -->
<!-- dod:end -->

## Aandachtspunten voor de reviewer

<!-- Risico's, keuzes of plekken waar je extra kritisch naar wilt laten kijken.
Raakt de wijziging autorisatie, pseudonimisering, cryptografie of BSN-verwerking?
Vraag dan een tweede reviewer met securitykennis. -->
