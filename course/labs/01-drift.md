# Lab 01 — Why Agents Drift

**Module:** 1 — Why Agents Drift
**Time:** 20 minutes
**File:** `main_local.py`

---

## What you will do

Run an ungrounded agent and ask it questions from the agentic-architecture domain. Record what it says. In Lab 02 you will ask the same questions of a grounded agent and compare.

---

## Step 1 — Read the file before you run it

Open `main_local.py`. Find the two questions the agent is asked:

```python
result = await agent.run("In one line: what is the medallion architecture?")
```

```python
async for update in agent.run(
    "Name three reasons to keep build-time and runtime agents separate.",
    stream=True,
):
```

Notice: no domain vocabulary is loaded. The agent has only its base training.

---

## Step 2 — Run it

```bash
OLLAMA_MODEL=qwen3.5:9b python main_local.py
```

---

## Step 3 — Record the answers

Write down (or screenshot) what the agent says about:
- The medallion architecture
- Build-time vs runtime agent separation

You will compare these answers in Lab 02. Pay attention to:
- Does it use the term "Coding Agent"? (It shouldn't — that's domain vocabulary.)
- Does it mention "SKILL"? (It shouldn't.)
- Does it invent plausible-sounding but wrong distinctions?

---

## Step 4 — Ask a domain question the script doesn't include

Add this question to the `main()` function in `main_local.py`:

```python
result = await agent.run(
    "What do we call the agent that reads a SKILL and emits artifacts?"
)
print("\n[domain] ", result)
```

Run again. Observe: the agent will invent an answer because it has no SKILL loaded.

---

## What just happened

The agent is `llm base + system prompt only`. There is no versioned vocabulary document, no rules, no out-of-scope definition. The model fills the gap with training data — which may be plausible but is not *your* vocabulary.

This is the gap the SKILL pattern closes.

---

## Exercise

Change the system prompt in `build_agent()`:

```python
instructions=(
    "You are a data-platform assistant. "
    "Answer in at most three sentences. If unsure, say so."
),
```

Replace it with something vaguer:

```python
instructions="You are a helpful assistant.",
```

Run again and compare. Notice how much the answer quality changes from just a system-prompt tweak — and how that tweak would need to be replicated in every agent you ever build.

The SKILL pattern solves this by externalising the vocabulary from the code entirely.

---

## Stretch goal

Ask the agent: *"What is the difference between a Coding Agent and a Runtime Agent?"*

Write down its answer. In Lab 04 you will see a Coding Agent produce a Runtime Agent. By then, you will know exactly how wrong (or accidentally right) this first answer was.

---

## Key terms introduced

| Term | Meaning |
|---|---|
| Ungrounded agent | An agent with no domain-specific vocabulary or rules loaded |
| Vocabulary drift | When a model uses generic or hallucinated terms instead of your domain's terms |
| System prompt | The developer-written instruction string baked into the agent — fragile, not versioned |
