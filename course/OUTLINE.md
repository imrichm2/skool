# AI Creating AI Agents — Skool Course Outline

Paste each section into Skool's course builder: Classroom → Modules → Add Module.
Each "Lesson" maps to one lesson card inside that module.

---

## COURSE TITLE
**AI Creating AI Agents** — Build, Ground, and Automate Runtime Agents with Microsoft Agent Framework

## COURSE SUBTITLE
Go from a hallucinating chatbot to a self-generating agent factory — using only local models and open-source tools.

## COURSE DESCRIPTION (for Skool "About" section)
Most agent tutorials show you how to call an API. This course shows you how to build agents that build agents.

You will learn the exact pattern that separates production agentic systems from demo chatbots: grounding agents in a versioned SKILL document, equipping them with real tools, and writing a Coding Agent that reads any SKILL and emits a working Runtime Agent in one command.

Every lesson is backed by running Python code you execute yourself. No cloud account required — all labs run on a local machine with Ollama.

By the end you will have:
- A grounded Runtime Agent that uses your domain vocabulary instead of hallucinated defaults
- A tool-augmented agent that calls real functions for live data
- A Coding Agent that reads a SKILL file and generates a new agent in seconds
- Your own SKILL file and its generated Runtime Agent — ready to iterate on

**Prerequisites:** Python 3.11+, basic async/await comfort, Git. No prior agent-framework experience needed.

---

## MODULE 1 — Why Agents Drift

**Module description:**
Before fixing a problem you need to feel it. In this module you run a real agent against questions from your domain and watch it hallucinate. You learn what "grounding" means, why it matters, and what the SKILL pattern solves.

### Lesson 1.1 — The Hallucination Gap
**Description:** Side-by-side: what a generic LLM says about your domain vocabulary vs what your documentation says. You will recognise this gap in your own org immediately.
**Learning objective:** Articulate why prompt-stuffing instructions into a system message is brittle, and why a versioned grounding document is better.

### Lesson 1.2 — Coding Agent vs Runtime Agent
**Description:** The most important distinction in agentic architecture. One builds artifacts; one serves users. Conflating them causes every wrong architecture decision that follows.
**Learning objective:** Correctly label any agent in a real system as Coding Agent or Runtime Agent, and explain why the distinction matters for audit, cost, and ownership.

### Lesson 1.3 — Lab Preview: Running Your First Local Agent
**Description:** Install the environment, pull a model with Ollama, and run `main_local.py`. You ask it about your domain; it guesses. That guess is the baseline you will fix in Module 2.
**Learning objective:** Verify your environment is working and observe ungrounded agent behaviour firsthand.

---

## MODULE 2 — The SKILL: Grounding Your Agent

**Module description:**
A SKILL is a versioned, declarative document the agent reads before answering. It is the single mechanism that turns a generic LLM into a domain expert that uses your vocabulary, follows your rules, and refuses to invent authority. In this module you load one, modify it, and feel the difference immediately.

### Lesson 2.1 — Anatomy of a SKILL File
**Description:** Frontmatter (name, description, license), instruction body (vocabulary, rules, out-of-scope). Every field has a purpose; none is decoration.
**Learning objective:** Write a valid SKILL.md from scratch for a domain you know.

### Lesson 2.2 — Wiring a SKILL to an Agent
**Description:** `InlineSkill`, `SkillFrontmatter`, `SkillsProvider`, `context_providers=[]` — the four objects that attach a SKILL to an Agent. Verified from the installed package source; no guessing.
**Learning objective:** Wire an InlineSkill to an Agent and confirm it changes the model's answers.

### Lesson 2.3 — Inline vs File-Based Skills
**Description:** `InlineSkill` (Python, robust) vs `FileSkillsSource` (loads a SKILL.md from disk, better for version control). When to use each.
**Learning objective:** Switch between inline and file-based skill loading with one environment variable.

### Lesson 2.4 — Lab: Ground Your Agent
**Description:** Run `main_grounded.py`. Ask the same questions you asked in Module 1. Compare the answers. Then edit the SKILL's instructions and re-run to see the change propagate.
**Learning objective:** Modify a SKILL and observe the grounded agent adopt the new vocabulary without any code change.

---

## MODULE 3 — Tools: Agents That Reach for Real Data

**Module description:**
Grounding fixes vocabulary drift. Tools fix factual drift. When an agent can call a function — look up a table, fetch today's date, query a catalogue — it stops guessing. In this module you learn the exact tool registration API, add two tools to a grounded agent, and watch them fire.

### Lesson 3.1 — Why Tools Change Everything
**Description:** An agent without tools is a closed system. An agent with tools is a reasoning loop that queries the world. The difference in answer quality is not marginal — it is categorical.
**Learning objective:** Explain when a tool is the right answer vs when the SKILL alone is sufficient.

### Lesson 3.2 — The @tool Decorator: Verified API
**Description:** `@tool`, `Annotated[type, "description"]`, `FunctionTool`, `normalize_tools`. Every name was verified by reading the installed package source — not assumed. You will adopt the same discipline.
**Learning objective:** Register a function as a tool using the correct decorator and pass it to Agent correctly.

### Lesson 3.3 — Tool Design Rules
**Description:** Return strings (or JSON-serialisable dicts). Keep tool scope narrow. Name the tool after what it returns, not what it does. Write the docstring for the model, not for a human reader.
**Learning objective:** Design a tool the model will call correctly on the first try.

### Lesson 3.4 — Lab: Add Tools to Your Grounded Agent
**Description:** Run `main_tools.py`. Watch `get_today_date` and `lookup_unity_catalog_table` fire in response to natural-language questions. Then add a third tool of your own.
**Learning objective:** Write, register, and test a new tool end-to-end without touching the agent's system prompt.

---

## MODULE 4 — The Coding Agent: AI Writing AI

**Module description:**
This is where the loop closes. A Coding Agent reads a SKILL and emits a complete, runnable Runtime Agent Python file. The Coding Agent itself uses tools (read a file, write a file) and a meta-SKILL (the verified API, verbatim templates, syntax rules). You run it, inspect the output, and watch a second agent run the file that the first agent wrote.

### Lesson 4.1 — What Makes a Coding Agent Different
**Description:** It has no end users. Its output is an artifact, not a conversation. It must be deterministic enough to produce runnable code. Every one of those constraints shapes its design.
**Learning objective:** Describe the three design constraints on a Coding Agent and how they appear in the code.

### Lesson 4.2 — The Meta-SKILL: Grounding an Agent That Writes Agents
**Description:** The Coding Agent's instructions are not prose — they are verified API templates copied from the installed source. You will never let an LLM guess an API name again after this lesson.
**Learning objective:** Write a meta-SKILL whose instructions contain exact, verifiable code templates rather than prose descriptions.

### Lesson 4.3 — Syntax Validation as a Tool
**Description:** `write_agent_file` runs `ast.parse()` before writing. If the model produces a syntax error, the tool returns the error line and the model self-corrects in the same run. This is a general pattern: make tools that catch model mistakes rather than writing retry loops in the caller.
**Learning objective:** Explain why embedding validation in tools is more robust than wrapping `agent.run()` in a try/except.

### Lesson 4.4 — Lab: Run the Coding Agent
**Description:** Run `main_coding_agent.py SKILL.md`. Watch it call `read_skill_file`, then `write_agent_file`. Inspect `generated/main_agentic-architecture.py`. Run it. One command in, a running agent out.
**Learning objective:** Execute the full Coding Agent loop and explain every file it touches.

---

## MODULE 5 — Capstone: Your SKILL, Your Agent

**Module description:**
You have all the pieces. Now you build something real. Write a SKILL for a domain you own — a data product, an internal tool, a support workflow. Run the Coding Agent against it. Run the generated agent. Share your SKILL and your generated agent in the community classroom.

### Lesson 5.1 — Designing a SKILL for Your Domain
**Description:** Vocabulary section (5–8 terms, exactly), rules (4–6, concrete not vague), out-of-scope (what the agent must refuse), and when-you-don't-know (who to name instead). Templates and examples included.
**Learning objective:** Write a SKILL that a grounded agent uses to give answers your team would actually accept.

### Lesson 5.2 — Running the Full Stack on Your SKILL
**Description:** Drop your SKILL.md into the project, run the Coding Agent, run the generated file, iterate. The feedback loop is: edit SKILL → regenerate → re-run → compare.
**Learning objective:** Complete at least one full generate → run → evaluate cycle on your own SKILL.

### Lesson 5.3 — What Production Looks Like
**Description:** What changes when you go from this workshop to production: a Workflow for audit trail and human-in-the-loop, a versioned SKILL in a repo with a PR process, eval tests that catch SKILL drift. You have the vocabulary to ask for all of it now.
**Learning objective:** Map the workshop pattern onto your organisation's real constraints.

### Lesson 5.4 — Share Your Agent in the Community
**Description:** Post your SKILL.md and a screenshot of your generated agent answering a domain question in the Skool classroom. Peer feedback from cohort members.
**Learning objective:** Give and receive one piece of specific feedback on another learner's SKILL design.

---

## SKOOL SETUP CHECKLIST

- [ ] Create course under Classroom tab
- [ ] Upload a cover image (suggest: a diagram of Coding Agent → SKILL → Runtime Agent loop)
- [ ] Set drip schedule if async: Module 1 on day 0, Module 2 on day 2, Module 3 on day 4, Module 4 on day 7, Module 5 open on day 9
- [ ] Pin the setup lab (labs/00-setup.md) as a resource in Module 1
- [ ] Create a Community post "Share your SKILL" as the discussion thread for Module 5
- [ ] Add the GitHub repo link to every lesson that has a lab
