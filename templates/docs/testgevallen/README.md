# Logische testgevallen

Leg hier de logische testgevallen vast, één bestand per story of per onderwerp. Geef elk testgeval een
ID volgens het patroon `GBO-LTC-<nummer>` en zet dat ID in de naam of een annotatie van de
geautomatiseerde test (`// LTC: GBO-LTC-001`). Het testrapport bij elke release toont dan per testgeval
of er een test voor is en wat het resultaat was (kwaliteitsplan §3, traceerbaarheid; ICTU
Kwaliteitsaanpak M03).

Voorbeeld:

## GBO-LTC-001 Bevraging zonder geldige autorisatie wordt geweigerd

- Story: GBO-123
- Uitgangssituatie: een verzoek zonder geldig FSC-contract
- Actie: de afnemer doet een GraphQL-bevraging
- Verwacht resultaat: HTTP 403 en een logregel met resultaat "geweigerd"
