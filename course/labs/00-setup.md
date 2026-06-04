# Lab 00 — Environment Setup

Complete this before Module 1. Every subsequent lab assumes this is done.

---

## What you need

| Requirement | Minimum version | Check |
|---|---|---|
| Python | 3.11 | `python --version` |
| Git | any | `git --version` |
| Ollama | latest | `ollama --version` |
| RAM | 8 GB free | needed for the 9B model |
| Disk | 6 GB free | for model weights |

---

## Step 1 — Clone the repo

```bash
git clone https://github.com/imrichm2/skool.git
cd skool
```

---

## Step 2 — Create the virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Verify the install:

```bash
python -c "from agent_framework import Agent, tool; print('OK')"
```

Expected output: `OK`

---

## Step 3 — Install Ollama and pull the model

Install Ollama (Linux/Mac):

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the model used in all labs:

```bash
ollama pull qwen3.5:9b
```

This downloads ~6 GB. It only runs once.

Verify Ollama is running:

```bash
ollama list
```

You should see `qwen3.5:9b` in the list.

---

## Step 4 — Smoke test

```bash
OLLAMA_MODEL=qwen3.5:9b python main_local.py
```

Expected output (exact wording will vary):

```
[provider] ollama

[run]     The medallion architecture organises data into Bronze (raw),
          Silver (cleaned), and Gold (aggregated) layers.

[stream]  1. Build-time agents ...
```

If you see that, your environment is ready.

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'agent_framework'`**
You are not in the virtual environment. Run `source .venv/bin/activate` first.

**`Connection refused` or `OllamaError`**
Ollama is not running. Start it with `ollama serve` in a separate terminal, or check that the Ollama app is open on Mac/Windows.

**Model is slow**
`qwen3.5:9b` needs ~8 GB RAM. Close other applications. For a faster (lower quality) alternative use `ollama pull qwen2.5:3b` and set `OLLAMA_MODEL=qwen2.5:3b`.

---

## Directory map

```
ProjectAgent/
├── main_local.py          ← Module 1 lab: ungrounded baseline
├── main_grounded.py       ← Module 2 lab: SKILL grounding
├── main_tools.py          ← Module 3 lab: tool-augmented agent
├── main_coding_agent.py   ← Module 4 lab: Coding Agent
├── SKILL.md               ← the agentic-architecture SKILL
├── generated/             ← Coding Agent writes here
└── course/
    └── labs/              ← you are here
```
