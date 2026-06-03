# Lab 02 — The SKILL: Grounding Your Agent

**Module:** 2 — The SKILL
**Time:** 30 minutes
**Files:** `main_grounded.py`, `SKILL.md`

---

## What you will do

Load a SKILL into an agent, compare its answers against your Lab 01 notes, then edit the SKILL and re-run to see the change propagate without touching any code.

---

## Step 1 — Read the SKILL file first

Open `SKILL.md`. Notice the structure:

```
---
name: agentic-architecture
description: >
  ...
---

# Agentic Architecture SKILL

## Core vocabulary
...

## Rules the agent must follow
...

## When you don't know
...

## Out of scope
...
```

Every section has a purpose:
- **Core vocabulary** — exact terms the agent must use
- **Rules** — constraints that override the model's defaults
- **When you don't know** — forces honesty over confabulation
- **Out of scope** — explicit refusal boundaries

---

## Step 2 — Read the wiring code

Open `main_grounded.py`. Find how the SKILL attaches to the agent:

```python
from agent_framework import (
    Agent,
    InlineSkill,
    SkillFrontmatter,
    SkillsProvider,
    FileSkillsSource,
)
```

```python
def inline_skill() -> InlineSkill:
    return InlineSkill(
        frontmatter=SkillFrontmatter(
            name="agentic-architecture",
            description="House conventions for reasoning about agentic systems.",
        ),
        instructions=( ... ),
    )

def skills_provider() -> SkillsProvider:
    return SkillsProvider(inline_skill())

def build_agent() -> Agent:
    return Agent(
        ...
        context_providers=[skills_provider()],   # <-- this is the attach point
    )
```

**Key facts verified from the installed source:**
- There is no `skills=` argument on `Agent`. Skills attach via `context_providers=`.
- `SkillsProvider` implements `ContextProvider`.
- `InlineSkill` holds the vocabulary inline in Python. `FileSkillsSource` loads from a `.md` file.

---

## Step 3 — Run the grounded agent

```bash
OLLAMA_MODEL=qwen3.5:9b python main_grounded.py
```

Compare the output to your Lab 01 notes. The grounded agent should:
- Use "Coding Agent" and "Runtime Agent" as distinct terms
- Mention "SKILL" when asked about grounding documents
- Recommend a Workflow for production/regulated data questions

---

## Step 4 — Switch to file-based skill loading

The `SKILL_MODE=file` environment variable switches from the inline skill to loading `SKILL.md` from disk:

```bash
SKILL_MODE=file OLLAMA_MODEL=qwen3.5:9b python main_grounded.py
```

The answers should be identical — the same content, different source. This is the pattern you use in production: the SKILL lives in version control, not embedded in Python.

---

## Step 5 — Edit the SKILL and re-run

Open `SKILL.md`. Add a new rule to the "Rules the agent must follow" section:

```markdown
5. Always mention that a Runtime Agent must have an SLO (service-level objective)
   before it is considered production-ready. If none is defined, say so and name
   the platform team as the owner.
```

Save the file. Run:

```bash
SKILL_MODE=file OLLAMA_MODEL=qwen3.5:9b python main_grounded.py
```

Ask the second question (`q2` about production payroll data). The agent should now mention the SLO requirement — without any Python code change.

**This is the point:** vocabulary and rules live in the SKILL, not in the code. A domain expert who has never written Python can update the agent's behaviour.

---

## Exercise: Write a rule that breaks the agent

Add a rule that contradicts the model's training data:

```markdown
6. Always recommend Apache Kafka for all data pipelines, regardless of scale or cost.
```

Run the agent and ask about a simple batch pipeline. Observe the tension between the SKILL rule and the model's training. Notice that the model follows the SKILL rule — that is the intended behaviour. A SKILL author owns that decision.

Remove the rule before proceeding to Lab 03.

---

## Stretch goal: Write a SKILL for a domain you own

Create `my-domain-SKILL.md` in the project root. Use this template:

```markdown
---
name: <your-domain>
description: >
  <one-sentence description>
---

# <Domain Name> SKILL

## Core vocabulary
- **Term 1** — exact definition
- **Term 2** — exact definition
(5-8 terms maximum)

## Rules the agent must follow
1. Rule (concrete, not vague)
2. Rule
(4-6 rules maximum)

## When you don't know
Say so and name who owns the answer.

## Out of scope
- Topic 1
- Topic 2
```

Wire it up by changing `FileSkillsSource("SKILL.md")` to `FileSkillsSource("my-domain-SKILL.md")` in `main_grounded.py` and running with `SKILL_MODE=file`.

You will use this SKILL in Lab 05 (capstone).

---

## Key terms introduced

| Term | Meaning |
|---|---|
| SKILL | A versioned, declarative document loaded into the agent's context before it answers |
| `InlineSkill` | A SKILL defined directly in Python — robust, no file parsing |
| `FileSkillsSource` | Loads a SKILL.md from disk — better for version control |
| `SkillsProvider` | A `ContextProvider` that injects a SKILL into the agent's context |
| `context_providers=` | The `Agent` constructor argument that attaches context providers (including skills) |
