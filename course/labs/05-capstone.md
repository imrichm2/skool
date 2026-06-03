# Lab 05 — Capstone: Your SKILL, Your Agent

**Module:** 5 — Capstone
**Time:** 60 minutes
**Files:** your own `my-SKILL.md`, `main_coding_agent.py`

This lab has no fixed script to run. You design the SKILL, you run the Coding Agent, you evaluate the output. That is the point.

---

## The challenge

By the end of this lab you will have:

1. A `SKILL.md` for a domain you actually work in
2. A generated Runtime Agent that uses your SKILL's vocabulary
3. Evidence (a screenshot or terminal output) that the agent answers a domain question using your vocabulary instead of generic defaults
4. One piece of feedback on another learner's SKILL in the community

---

## Part A — Design your SKILL

Pick a domain you own or work in daily. Good candidates:

- A data product your team maintains (an analytics domain, a reporting layer)
- An internal tool or platform (a developer portal, a deployment pipeline)
- A business process (a customer support workflow, an onboarding checklist)
- A technical domain you are the expert in (Kubernetes operations, dbt modelling, data contracts)

**Avoid:** domains that are too broad ("software engineering") or too narrow ("one specific table"). Aim for a domain where you could write a 1-page style guide that a new team member would find useful.

---

### SKILL template

Create `my-SKILL.md` in the project root:

```markdown
---
name: <kebab-case-name>
description: >
  <One sentence: what domain this covers and who benefits from it.>
license: internal
---

# <Domain Name> SKILL

## Core vocabulary
(5–8 terms. Each term gets one sentence. Be exact.)

- **Term** — definition the agent must use, not a generic synonym
- **Term** — definition

## Rules the agent must follow
(4–6 rules. Concrete, not vague. Each rule must change agent behaviour.)

1. Rule
2. Rule

## When you don't know
<Who owns the answer the agent doesn't have? Name a team or role.>
Say so plainly and name the owner. Never invent an authority.

## Out of scope
(What must the agent refuse or escalate?)

- Topic 1
- Topic 2
```

**SKILL design checklist:**

- [ ] Every vocabulary term would be wrong if the agent used a generic synonym
- [ ] Every rule changes something the LLM would otherwise do differently
- [ ] The "when you don't know" section names a real person or team role
- [ ] At least one "out of scope" item is something the LLM would happily discuss without the SKILL

---

## Part B — Run the Coding Agent on your SKILL

```bash
OLLAMA_MODEL=qwen3.5:9b python main_coding_agent.py my-SKILL.md
```

Check the output:

```bash
python -c "import ast; ast.parse(open('generated/main-<name>.py').read()); print('syntax OK')"
```

Run it:

```bash
OLLAMA_MODEL=qwen3.5:9b python generated/main-<name>.py
```

---

## Part C — Evaluate the generated agent

Ask the generated agent three questions:

**Question 1 — vocabulary test**
Ask for the definition of one of your core vocabulary terms. Does the agent use your exact definition, or a generic synonym?

**Question 2 — rules test**
Ask something that should trigger one of your rules. Does the agent follow the rule, or drift back to the LLM default?

**Question 3 — out-of-scope test**
Ask about something in your "Out of scope" section. Does the agent decline and name the right owner?

Fill in this scorecard:

| Test | Expected | Actual | Pass? |
|---|---|---|---|
| Vocabulary: `<term>` | `<your definition>` | | |
| Rule: `<rule number>` | | | |
| Out of scope: `<topic>` | Decline + escalate | | |

If any test fails, the SKILL instruction is the fix — not the agent code. Edit `my-SKILL.md`, re-run the Coding Agent, re-run the generated agent, re-score.

---

## Part D — Iterate

This is the core workflow you will repeat in production:

```
Edit SKILL.md
    ↓
python main_coding_agent.py my-SKILL.md
    ↓
python generated/main-<name>.py
    ↓
Run the three evaluation questions
    ↓
Score → if any fail, back to top
```

Run at least two iteration cycles before moving to Part E. Note what you changed between runs and why.

---

## Part E — Share in the community

Post in the Skool classroom thread **"Share your SKILL"**:

1. Your `my-SKILL.md` file contents (paste as code block)
2. One screenshot or terminal paste showing the agent answering a domain question with your vocabulary
3. One sentence: what surprised you when the generated agent first ran

Then find one other learner's post and leave feedback using this format:

> **Vocabulary:** [one term that is well-defined / one that could be sharper]
> **Rules:** [one rule that is concrete / one that is still vague]
> **Suggestion:** [one specific change that would improve the SKILL]

---

## What production looks like from here

You now have the pattern. Here is what changes at production scale:

**Version control the SKILL**
`my-SKILL.md` goes into a Git repo with a PR process. Domain experts review SKILL changes; engineers review generated code. The Coding Agent runs in CI on every SKILL merge.

**Eval tests catch drift**
Write two or three eval questions per SKILL (like your Part C scorecard). Run them automatically on every generated agent to catch regressions.

**Workflow for regulated outputs**
If the generated agent touches regulated data, the Coding Agent run is wrapped in a `WorkflowBuilder` step with a human-in-the-loop approval gate before the file is written to the repo.

**Multiple SKILLs, one Coding Agent**
The Coding Agent is domain-agnostic. One `main_coding_agent.py` generates agents for every domain in your organisation, as long as each domain has a SKILL file.

---

## Graduation criteria

You have completed the course when you can answer yes to all of these:

- [ ] I can explain the difference between a Coding Agent and a Runtime Agent to a colleague in one minute
- [ ] I can write a SKILL for any domain I own, in under 30 minutes
- [ ] I know the exact `@tool` and `Agent()` API (not guessing from memory — verified from source)
- [ ] I have run the Coding Agent end-to-end and have a generated, running Runtime Agent on my machine
- [ ] I know what a Workflow is for and why a bare Runtime Agent is not sufficient for regulated data flows
