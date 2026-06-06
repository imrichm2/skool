# Build AI Agents at Home

Companion repo for the **[AI Creating AI Agents](https://www.skool.com/ai-agents-4094/about)** Skool course.

Go from a hallucinating chatbot to a self-generating agent factory — using only local models and open-source tools.

## Join the course

**[skool.com/ai-agents-4094/about](https://www.skool.com/ai-agents-4094/about)** — community, lessons, and structured labs.

## Quick start

```bash
git clone https://github.com/imrichm2/skool.git
cd skool
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen3.5:9b
python main_local.py
```

> **Windows:** replace `source .venv/bin/activate` with `.venv\Scripts\activate`

## What's here

| File | Module | What it does |
|---|---|---|
| `main_local.py` | 1 — Drift | Ungrounded baseline — watch it hallucinate |
| `main_grounded.py` | 2 — SKILL | Agent grounded with a versioned SKILL document |
| `main_tools.py` | 3 — Tools | Tool-augmented agent that calls real functions |
| `main_coding_agent.py` | 4 — Coding Agent | AI that reads a SKILL and writes a Runtime Agent |
| `SKILL.md` | All | The agentic-architecture SKILL used throughout |
| `generate_cover.py` | — | Regenerates the Skool cover image |
| `course/OUTLINE.md` | — | Full Skool module + lesson structure |
| `course/labs/` | 1–5 | Step-by-step lab instructions per module |

## Labs

Start here: [`course/labs/00-setup.md`](course/labs/00-setup.md)

| Lab | File | Time |
|---|---|---|
| 00 Setup | `course/labs/00-setup.md` | 10 min |
| 01 Why agents drift | `course/labs/01-drift.md` | 20 min |
| 02 The SKILL | `course/labs/02-skill.md` | 30 min |
| 03 Tools | `course/labs/03-tools.md` | 35 min |
| 04 Coding Agent | `course/labs/04-coding-agent.md` | 40 min |
| 05 Capstone | `course/labs/05-capstone.md` | 60 min |

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com) with `qwen3.5:9b` pulled
- 8 GB RAM free for the 9B model (use `qwen2.5:3b` on smaller machines)

## Key concepts

| Term | Meaning |
|---|---|
| **Coding Agent** | Build-time agent that reads a SKILL and emits artifacts. Does NOT serve end users. |
| **Runtime Agent** | The agent the business operates. Output of the Coding Agent. |
| **SKILL** | Versioned declarative document loaded into the agent's context before it answers. |
| **Workflow** | Orchestration layer with human-in-the-loop and checkpointing — for regulated data. |

## License

MIT
