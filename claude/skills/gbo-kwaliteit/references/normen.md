# GBO-normen (samenvatting)

Bron van waarheid: https://github.com/ICTU/GBO-quality/blob/main/docs/kwaliteitsplan.md.
Bij verschil geldt het kwaliteitsplan.

| Norm | Waarde |
|---|---|
| Cyclomatische complexiteit per methode | ≤ 10 |
| Duplicatie | 0% |
| Omvang per methode | ≤ 20 statements |
| Parameters per methode | ≤ 5 |
| Unit-testdekking nieuwe code | ≥ 80% |
| Functionele testdekking | ≥ 80% van de logische testgevallen geautomatiseerd |
| Kwetsbaarheden | Geen critical/high zonder geaccepteerde uitzondering |
| Secrets in code | Nul |
| Toegankelijkheid (UI) | WCAG 2.2 AA, geen axe-overtredingen |
| Review | Minimaal 1 andere ontwikkelaar; 2 bij autorisatie, pseudonimisering, cryptografie, BSN |
| Dependencies | Vastgepind; updates via Dependabot met 14 dagen cooldown |
| Hersteltermijn kwetsbaarheden | Hoge kans op misbruik én hoge schade: patchrelease of mitigatieadvies binnen 1 week |
| Pentest internetfacing componenten | Bij elke nieuwe release of major update; hoog risico zonder mitigatie blokkeert productie |
| Logging | Actie, object, resultaat, oorsprong, actor, tijdstempel; nooit BSN's, wachtwoorden, tokens of sleutels |
| Cryptografie | Volgens NCSC-adviezen, via bewezen bibliotheken; sleutels nooit in de code |
| Toegang | MFA verplicht voor GitHub en ontwikkeltooling; wekelijkse automatische toegangscontrole |
| Kwetsbaarheden-issues | Nachtelijke/wekelijkse scan maakt issue met deadline 7 dagen; risicoafweging in het issue |
| Uitzondering kwetsbaarheid | In `.trivyignore` met reden, issue en `exp:JJJJ-MM-DD` |
| Bewijs per release | Testrapport en bewijsbundel automatisch; rollbackinstructie in `docs/rollback.md` |
| Kwaliteitskalender | Pentest en self-assessment halfjaarlijks; toegangsrechten per kwartaal; register, training en risicoanalyses jaarlijks |
