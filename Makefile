# Makefile — entrate rapide per il tooling della repo isola_i3v_visual.
# (blindatura 2026-06)

.PHONY: help deps audit audit-fast test test-all catalogo briefs volume1 check routing dashboard sync

help:
	@echo "Target disponibili:"
	@echo "  make deps       — installa dipendenze (requirements + dev)"
	@echo "  make audit      — audit 1..4 (grafo + prosa)"
	@echo "  make audit-fast — audit 1..3 (salta prosa)"
	@echo "  make test       — pytest veloce (non slow, ~3s)"
	@echo "  make test-all   — pytest completo (build PDF reale, ~60s)"
	@echo "  make check      — test + audit (il cancello pre-push)"
	@echo "  make catalogo   — rigenera catalogo_web/data/entities.json"
	@echo "  make briefs     — rigenera i 12 writing brief"
	@echo "  make volume1    — build PDF volume 1 in _output/"
	@echo "  make routing    — rigenera la tabella di routing nel CLAUDE.md dai frontmatter skill"
	@echo "  make dashboard  — rigenera i dati della dashboard di sistema (dashboard/)"
	@echo "  make sync       — rigenera tutto il derivato (catalogo+briefs+routing+dashboard); git status = report"

deps:
	python3 -m pip install -r requirements.txt -r requirements-dev.txt

audit:
	python3 scripts/audit/run_all_audits.py

audit-fast:
	python3 scripts/audit/run_all_audits.py --fast

test:
	python3 -m pytest tests/ -m "not slow" -q

test-all:
	python3 -m pytest tests/ -q

check: test audit

catalogo:
	python3 scripts/build_catalogo_web.py

briefs:
	python3 scripts/build_writing_brief.py --all

volume1:
	python3 scripts/build_volume.py --volume 1

routing:
	python3 scripts/build_routing_table.py --apply

dashboard:
	python3 scripts/build_dashboard.py

# sync: rigenera tutto il derivato. Essendo gli script idempotenti,
# il `git status` dopo il sync mostra esattamente cosa era disallineato.
sync: catalogo briefs routing dashboard
	@echo ""
	@echo "Sync completato — 'git status' mostra cosa era disallineato:"
	@git status --short
