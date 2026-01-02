# ===== Makefile (living-vote-core-proof) =====
.DEFAULT_GOAL := help
SHELL := /bin/bash

POETRY ?= poetry
ARGS ?=

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
.PHONY: help
help: ## Show available targets
	@awk 'BEGIN {FS=":.*##"; printf "\nTargets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ {printf "  %-18s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: info
info: ## Show environment info (Poetry, Python)
	@$(POETRY) --version
	@$(POETRY) run python --version

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------
.PHONY: install
install: ## Install dependencies (poetry install)
	@$(POETRY) install

.PHONY: lock
lock: ## Update lock file (poetry lock)
	@$(POETRY) lock

.PHONY: update
update: ## Update dependencies (poetry update)
	@$(POETRY) update

.PHONY: shell
shell: ## Spawn a Poetry shell
	@$(POETRY) shell

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
.PHONY: test
test: ## Run pytest (quiet)
	@$(POETRY) run pytest -q $(ARGS)

.PHONY: test-verbose
test-verbose: ## Run pytest (verbose)
	@$(POETRY) run pytest -vv $(ARGS)

.PHONY: test-fast
test-fast: ## Run pytest (stop after first failure)
	@$(POETRY) run pytest -q --maxfail=1 $(ARGS)

# ----------------------------------------------------------------------
# Quality (minimal, no extra deps required)
# ----------------------------------------------------------------------
.PHONY: compile
compile: ## Byte-compile to catch syntax errors early
	@$(POETRY) run python -m compileall -q living_vote

.PHONY: check
check: compile test ## Run minimal CI checks (compile + tests)

# ----------------------------------------------------------------------
# Cleaning
# ----------------------------------------------------------------------
.PHONY: clean
clean: ## Remove caches and build artifacts
	@rm -rf .pytest_cache .mypy_cache .ruff_cache
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

# ----------------------------------------------------------------------
# Convenience
# ----------------------------------------------------------------------
.PHONY: tree
tree: ## Show project tree (if 'tree' is installed)
	@if command -v tree >/dev/null 2>&1; then tree -a -I ".venv|.git"; else echo "tree not installed"; fi
