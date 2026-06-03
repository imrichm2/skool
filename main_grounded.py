"""
SKILL-grounded Runtime Agent — Agentic Architecture domain.

This is the article's Layer-1 idea working for real: the agent reads a SKILL
into its context BEFORE answering, so it uses house vocabulary and rules
instead of generic (often hallucinated) LLM defaults.

VERIFIED against the installed agent-framework (the API is experimental, so
this was introspected, not guessed):
  - There is NO `skills=` argument on Agent. Skills attach via the
    `context_providers=` argument, because SkillsProvider IS a ContextProvider.
  - Build a skill with InlineSkill(frontmatter=SkillFrontmatter(...),
    instructions=...), OR load SKILL.md files with FileSkillsSource(paths).
  - Wrap skill(s) or a source in SkillsProvider(...), pass it to
    context_providers=[...].

Run:
  make run-grounded            # if you add the target, see README
  # or directly, with the same env as main_local.py:
  OLLAMA_MODEL=llama3.1:8b .venv/bin/python main_grounded.py

NOTE ON MODEL CHOICE: grounding helps, but a 3B model (llama3.2) still drifts.
For a convincing demo use a stronger local model (llama3.1:8b / qwen2.5) or
point at Foundry. Set SKILL_MODE=file to use the SKILL.md on disk instead of
the inline skill.
"""

import os
import asyncio

from agent_framework import (
    Agent,
    InlineSkill,
    SkillFrontmatter,
    SkillsProvider,
    FileSkillsSource,
)


# --- provider (same swap logic as main_local.py) ---------------------------
def build_client():
    provider = os.environ.get("PROVIDER", "ollama").lower()
    if provider == "openai":
        from agent_framework.openai import OpenAIChatClient
        return OpenAIChatClient(
            model=os.environ.get("OPENAI_MODEL", "gpt-4.1"),
            api_key=os.environ["OPENAI_API_KEY"],
        )
    from agent_framework.ollama import OllamaChatClient
    return OllamaChatClient(
        host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        model=os.environ.get("OLLAMA_MODEL", "llama3.2"),
    )


# --- the SKILL, two ways ---------------------------------------------------
def inline_skill() -> InlineSkill:
    """Skill defined right here in Python. Robust, no file parsing."""
    return InlineSkill(
        frontmatter=SkillFrontmatter(
            name="agentic-architecture",
            description="House conventions for reasoning about agentic systems.",
        ),
        instructions=(
            "Use this vocabulary exactly:\n"
            "- Coding Agent = build-time agent that reads a SKILL and emits "
            "artifacts (code, agent defs, workflows, tools, evals). It does not "
            "serve end users.\n"
            "- Runtime Agent = the agent the business operates and users talk "
            "to; it is the OUTPUT of the Coding Agent.\n"
            "- SKILL = the versioned document the Coding Agent reads first.\n"
            "- Workflow = orchestration with human-in-the-loop and checkpointing.\n"
            "Rules: never conflate Coding and Runtime agents. The SDK is "
            "provider-agnostic (Ollama/OpenAI/Foundry is a one-line change). "
            "For regulated/production data flows, require an audit trail and "
            "human-in-the-loop, and say that belongs in a Workflow. If you "
            "don't know, say so and name the owner (platform/governance/infra). "
            "Never invent an authority or standard to sound credible."
        ),
    )


def skills_provider() -> SkillsProvider:
    mode = os.environ.get("SKILL_MODE", "inline").lower()
    if mode == "file":
        # Parses frontmatter + body from the SKILL.md on disk.
        source = FileSkillsSource("skills/agentic-architecture/SKILL.md")
        return SkillsProvider(source)
    return SkillsProvider(inline_skill())


def build_agent() -> Agent:
    return Agent(
        name="AgenticArchitectAdvisor",
        instructions=(
            "You are an agentic-architecture advisor. Follow the loaded SKILL's "
            "vocabulary and rules exactly. Keep answers under four sentences."
        ),
        client=build_client(),
        context_providers=[skills_provider()],   # <-- this is how skills attach
    )


async def main() -> None:
    print(f"[provider] {os.environ.get('PROVIDER', 'ollama')}  "
          f"[skill_mode] {os.environ.get('SKILL_MODE', 'inline')}")
    agent = build_agent()

    # A question the SKILL has strong opinions about. A grounded agent should
    # answer using the Coding/Runtime distinction, NOT invent a definition.
    q1 = ("We need an agent that generates other agents from a spec. "
          "Which layer is that, and what does it produce?")
    print("\n[Q1]", q1)
    print("[A1]", await agent.run(q1))

    # A question that should trigger the audit-trail / Workflow rule.
    q2 = ("How should we run an agent that moves production payroll data?")
    print("\n[Q2]", q2)
    print("[A2]", await agent.run(q2))


if __name__ == "__main__":
    asyncio.run(main())
