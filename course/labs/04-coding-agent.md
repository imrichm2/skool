# Lab 04 — The Coding Agent: AI Writing AI

**Module:** 4 — The Coding Agent
**Time:** 40 minutes
**File:** `main_coding_agent.py`

---

## What you will do

Run a Coding Agent that reads a SKILL file and writes a complete Runtime Agent Python script. Inspect the generated file. Run the generated agent. Understand every design decision in the Coding Agent.

---

## Step 1 — Read the architecture before running

Open `main_coding_agent.py`. The Coding Agent has:

**Two tools:**

```python
@tool
def read_skill_file(path: Annotated[str, "Path to the SKILL.md file"]) -> str:
    """Read a SKILL file from disk and return its full contents."""
    ...

@tool
def write_agent_file(filename: Annotated[str, "Output filename"],
                     content: Annotated[str, "Python source code"]) -> str:
    """Validate syntax then write the Runtime Agent script to generated/."""
    import ast
    try:
        ast.parse(content)
    except SyntaxError as exc:
        return f"SYNTAX ERROR at line {exc.lineno}: {exc.msg} ..."
    # ... write to disk
```

**A meta-SKILL in its instructions:**

The `META_SKILL` string contains:
- Exact import statements to use
- A verbatim `build_client()` template
- `@tool` and `Agent()` usage examples
- Required file structure (8 sections, in order)
- The triple-quote prohibition (use parenthesised single-quoted strings)

This is not prose — it is verified code, copied from the installed package source and embedded in the agent's instructions.

**Why is `write_agent_file` different from a simple file write?**

It runs `ast.parse()` on the content first. If the model produces a syntax error, the tool returns the error back to the model, which self-corrects in the same run. You do not need a retry loop in the caller — the tool loop handles it.

---

## Step 2 — Run the Coding Agent

```bash
OLLAMA_MODEL=qwen3.5:9b python main_coding_agent.py SKILL.md
```

Watch the output. The Coding Agent will:
1. Call `read_skill_file("SKILL.md")`
2. Parse the frontmatter to extract `name: agentic-architecture`
3. Generate the Runtime Agent script
4. Call `write_agent_file("main_agentic-architecture.py", <content>)`

The generated file lands in `generated/main_agentic-architecture.py`.

---

## Step 3 — Inspect the generated file

```bash
cat generated/main_agentic-architecture.py
```

Verify it contains:
- [ ] Module docstring on line 1
- [ ] `import os, asyncio` and `from typing import Annotated`
- [ ] `build_client()` with the correct Ollama/OpenAI swap pattern
- [ ] At least one `@tool`-decorated function
- [ ] `skills_provider()` using `InlineSkill` + `SkillsProvider`
- [ ] `build_agent()` with `tools=` and `context_providers=`
- [ ] `async main()` that starts with `agent = build_agent()`

Also check for syntax validity:

```bash
python -c "import ast; ast.parse(open('generated/main_agentic-architecture.py').read()); print('syntax OK')"
```

---

## Step 4 — Run the generated agent

```bash
OLLAMA_MODEL=qwen3.5:9b python generated/main_agentic-architecture.py
```

The generated Runtime Agent answers questions using the vocabulary from `SKILL.md`. You wrote no agent code — the Coding Agent wrote it for you.

---

## Step 5 — Dry-run mode

Use `--dry-run` to print the generated code without writing it to disk:

```bash
OLLAMA_MODEL=qwen3.5:9b python main_coding_agent.py --dry-run SKILL.md
```

This is useful for reviewing the output before committing it, or for understanding what the Coding Agent would produce for a new SKILL without overwriting an existing file.

---

## Exercise: Trace a tool call

Add a print statement inside `write_agent_file` (before the `ast.parse` call) to log when it is called:

```python
print(f"\n[TOOL CALL] write_agent_file(filename={filename!r}, content_length={len(content)})")
```

Run the Coding Agent again. You will see exactly when in the conversation loop the tool fires. Notice it fires only once (or twice if the first attempt has a syntax error and the model retries).

Remove the print statement when done.

---

## Exercise: Force a syntax error and watch the self-correction

Temporarily change `META_SKILL` so the last line of the required structure section reads:

```
Section 7: async main() — use triple-quoted strings freely.
```

Run the Coding Agent. If the model follows this bad instruction and produces a syntax error, `write_agent_file` will return the error message, and the model will attempt to fix and resubmit. Watch the conversation loop handle it automatically.

Restore the correct instruction when done.

---

## What makes this a Coding Agent (not a Runtime Agent)

| Property | Coding Agent | Runtime Agent |
|---|---|---|
| Who calls it | Developer / CI pipeline | End user |
| Output | Python file on disk | Conversation response |
| Has end users | No | Yes |
| Needs audit trail | Yes, in production | Yes, if regulated data |
| Tools it uses | File I/O | Domain data (catalogue, APIs) |

In production, the Coding Agent run would be wrapped in a Workflow with a human-in-the-loop review step before the generated file is merged to the repo.

---

## Stretch goal: Point at a different SKILL

Create a new minimal SKILL file:

```bash
cat > /tmp/support-SKILL.md << 'EOF'
---
name: customer-support
description: Vocabulary and rules for a customer support Runtime Agent.
---

# Customer Support SKILL

## Core vocabulary
- **Ticket** — a customer-reported issue with a unique ID
- **Escalation** — routing a ticket to a human agent when the bot cannot resolve it
- **SLA** — service-level agreement defining maximum response time

## Rules
1. Never promise a resolution time unless the SLA is explicitly stated.
2. Always offer to escalate if the issue is unresolved after two clarification turns.
3. Do not discuss pricing or billing — escalate to billing team.

## When you don't know
Say so and offer to escalate.

## Out of scope
- Billing and pricing
- Technical integrations not mentioned in this SKILL
EOF
```

Run the Coding Agent on it:

```bash
OLLAMA_MODEL=qwen3.5:9b python main_coding_agent.py /tmp/support-SKILL.md
```

Inspect `generated/main_customer-support.py`. Run it. The loop closes on a completely different domain — without any code change to the Coding Agent.

---

## Key terms introduced

| Term | Meaning |
|---|---|
| Coding Agent | A build-time agent whose output is an artifact (code, config, workflow), not a conversation |
| Meta-SKILL | The Coding Agent's own grounding document — contains verified API templates rather than prose |
| `ast.parse()` | Python's built-in syntax checker — used in `write_agent_file` to catch LLM-generated syntax errors before writing |
| Self-correction loop | When a tool returns an error, the agent framework's tool loop feeds it back to the model, which retries — no caller retry code needed |
| `--dry-run` | Runs the Coding Agent without writing the file; output is printed to stdout for review |
