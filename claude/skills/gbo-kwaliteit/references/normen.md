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
