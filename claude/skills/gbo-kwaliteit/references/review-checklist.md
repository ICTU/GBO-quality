# Review-checklist

Gebaseerd op de checklist in het ICTU-template kwaliteitsplan, aangevuld voor GBO.

1. **Voorbereiden:** lees de story en acceptatiecriteria, en de relevante delen van het ontwerp
   (GO, PSA, technisch ontwerp). Bedenk hoe je het zelf zou bouwen.
2. **Functionaliteit:** sluit de code aan bij de story? Zijn randgevallen en foutafhandeling meegenomen?
3. **Codekwaliteit:** leesbaar, consistent met de codeerstandaard, geen duplicatie of onnodige complexiteit,
   betekenisvolle namen.
4. **Onderhoudbaarheid:** goed testbaar, unit- en integratietests aanwezig, logische structuur.
5. **Veiligheid en betrouwbaarheid:**
   - geen hardcoded secrets of credentials;
   - inputvalidatie en foutafhandeling, ook voor GraphQL-queries (diepte, complexiteit, introspectie in productie);
   - autorisatie wordt per verzoek afgedwongen (PEP), niet alleen in de UI of client;
   - dataminimalisatie: alleen gegevens die binnen grondslag of toestemming vallen;
   - geen BSN's of persoonsgegevens in logging, foutmeldingen of tests;
   - cryptografie via bewezen bibliotheken, geen eigen implementaties.
6. **Performance:** geen onnodig zware operaties (bijv. N+1-queries in resolvers), efficiënt gebruik van resources.
7. **Overig:** alle tests slagen; documentatie, schema's en conformancetests zijn bijgewerkt.
