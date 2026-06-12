# skills/ — indice delle skill

**Una sessione = una skill.** Identifica il ruolo, leggi la sua `SKILL.md`, stai nel suo scope. Le **regole comuni** (non-danno, tre fonti, comunicazione con Ray, matrice di propagazione) vivono in **un solo posto: `CLAUDE.md`** in root — leggilo prima della skill.

**Convenzione:** ogni skill è `skills/<ruolo>/SKILL.md`, con frontmatter YAML (`role`, `trigger`, `scope_write`, `commands`, `order`). La **tabella di routing** nel `CLAUDE.md` è generata dai frontmatter: `make routing` (mai editarla a mano).

| Skill | File |
|---|---|
| brieffer | `brieffer/SKILL.md` |
| prosa | `prosa/SKILL.md` |
| canonizzatore | `canonizzatore/SKILL.md` (puntatore a `_visual_pipeline/`) |
| visual | `visual/SKILL.md` (+ sotto-skill `visual/compilatore.md`) |
| illustratore | `illustratore/SKILL.md` |
| scenografo | `scenografo/SKILL.md` |
| cartografo | `cartografo/SKILL.md` |
| contributore | `contributore/SKILL.md` |

Se un task ricade fra due skill: **fermati e segnala a Ray** (splittare in due sessioni o eccezione ragionata).

Per aggiungere una skill nuova: crea `skills/<ruolo>/SKILL.md` col frontmatter standard, poi `make routing`.
