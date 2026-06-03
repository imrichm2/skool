# Tiny Makefile for the Hello Runtime Agent.
# One command on a fresh Ubuntu box:  make run-local

VENV    := .venv
PY      := $(VENV)/bin/python
PIP     := $(VENV)/bin/pip
MODEL   ?= llama3.2

.DEFAULT_GOAL := run-local

# --- environment -----------------------------------------------------------
$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install --quiet --upgrade pip

.PHONY: install-local
install-local: $(VENV)/bin/activate
	$(PIP) install --quiet agent-framework-core
	$(PIP) install --quiet --pre agent-framework-ollama   # beta -> needs --pre

.PHONY: install-openai
install-openai: $(VENV)/bin/activate
	$(PIP) install --quiet agent-framework-core agent-framework-openai

# --- ollama: install if missing, pull the model if missing -----------------
.PHONY: ollama
ollama:
	@command -v ollama >/dev/null 2>&1 || { \
		echo ">> installing ollama"; curl -fsSL https://ollama.com/install.sh | sh; }
	@ollama list 2>/dev/null | grep -q "$(MODEL)" || { \
		echo ">> pulling model $(MODEL)"; ollama pull $(MODEL); }

# --- run --------------------------------------------------------------------
.PHONY: run-local
run-local: install-local ollama
	OLLAMA_MODEL=$(MODEL) $(PY) main_local.py

.PHONY: run-openai
run-openai: install-openai
	@test -n "$$OPENAI_API_KEY" || { echo "set OPENAI_API_KEY first"; exit 1; }
	PROVIDER=openai $(PY) main_local.py

.PHONY: clean
clean:
	rm -rf $(VENV) __pycache__
