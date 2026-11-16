# CLAUDE.md

De gedeelde instructies voor alle AI-assistenten staan in AGENTS.md:

@AGENTS.md

## Alleen voor Claude Code

- De skill `gbo-kwaliteit` in `.claude/skills/` bevat de werkwijze uit het GBO-kwaliteitsplan.
  Gebruik die skill bij het committen, het voorbereiden van een pull request en bij een release.
- De hook in `.claude/hooks/` blokkeert `--no-verify` en force-pushes naar main, en draait pre-commit
  vóór elke commit.
