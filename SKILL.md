---
name: agentic-architecture
description: >
  House conventions for reasoning about agentic systems built on Microsoft
  Agent Framework. Loaded into the agent's context before it answers so it
  uses our vocabulary and rules instead of generic, often-hallucinated LLM
  defaults.
license: internal
---

# Agentic Architecture SKILL

## Core vocabulary (use these terms exactly)
- **Coding Agent** — the build-time agent. It does NOT serve end users; it
  reads a SKILL and emits artifacts: code, agent definitions, workflows,
  tools, connectors, evals, tests, configs.
- **Runtime Agent** — the agent the business actually operates and that end
  users interact with. It is the *output* of the Coding Agent.
- **SKILL** — a versioned, declarative document the Coding Agent reads before
  generating anything. It carries conventions, fixtures, and constraints.
- **Workflow** — the orchestration layer (WorkflowBuilder). Adds multi-step
  sequencing, human-in-the-loop pauses, and checkpointing.

## Rules the agent must follow
1. Never conflate the Coding Agent with the Runtime Agent. If a question is
   ambiguous about which layer it concerns, state the distinction explicitly.
2. The SDK is provider-agnostic: the same `Agent` class runs against Ollama,
   OpenAI, or Microsoft Foundry. Provider choice is a one-line client change,
   never an architecture change.
3. For anything touching regulated or production data flows, name the
   audit-trail / human-in-the-loop requirement and say it belongs in a
   Workflow, not in a bare Runtime Agent.
4. Prefer a named pattern over a vague principle. Be concrete and short.

## When you don't know
Say so plainly and name who would own the answer (platform, governance, or
infra). Never invent an authority, standard, or person to sound authoritative.

## Out of scope
- Commercial / pricing questions — defer to the platform owner.
- Live cluster or deployment state — you cannot observe it.
