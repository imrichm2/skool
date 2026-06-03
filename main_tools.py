"""
Tool-augmented Runtime Agent — adds callable tools to the skill-grounded agent.

API verified from installed agent_framework source (_tools.py, _agents.py):
  - Decorator: @tool  (agent_framework._tools, re-exported at top level)
    No args form: uses function __name__ as tool name, docstring as description.
    Parameter descriptions via Annotated[type, "description string"].
  - Registration: Agent(tools=[...], ...)
    Accepts FunctionTool instances, plain callables (auto-wrapped), or both.
    Per-call override is also possible via agent.run(tools=[...]).
  - Return values are auto-serialized to str by FunctionTool.parse_result().
  - No @ai_function — that decorator does not exist in this package.

Run:
  OLLAMA_MODEL=qwen3.5:9b .venv/bin/python main_tools.py
"""

import os
import asyncio
import json
from datetime import date
from typing import Annotated

from agent_framework import (
    Agent,
    InlineSkill,
    SkillFrontmatter,
    SkillsProvider,
    FileSkillsSource,
    tool,
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


# --- tools -----------------------------------------------------------------

@tool
def get_today_date() -> str:
    """Return today's date in ISO 8601 format (YYYY-MM-DD)."""
    return date.today().isoformat()


@tool
def lookup_unity_catalog_table(
    name: Annotated[str, "Fully-qualified table name, e.g. catalog.schema.table"],
) -> str:
    """Look up metadata for a Unity Catalog table and return a JSON summary."""
    parts = (name.split(".") + ["", "", ""])[:3]
    catalog, schema, table = parts
    return json.dumps(
        {
            "table": name,
            "catalog": catalog or "main",
            "schema": schema or "default",
            "table_name": table or name,
            "format": "delta",
            "columns": [
                {"name": "id",         "type": "bigint",    "nullable": False},
                {"name": "event_time", "type": "timestamp", "nullable": False},
                {"name": "payload",    "type": "string",    "nullable": True},
            ],
            "owner": "data-platform-team",
            "location": (
                f"abfss://bronze@datalake.dfs.core.windows.net/{table or name}/"
            ),
            "properties": {
                "delta.minReaderVersion": "1",
                "delta.minWriterVersion": "2",
            },
        },
        indent=2,
    )


# --- SKILL (kept from main_grounded.py) ------------------------------------
def inline_skill() -> InlineSkill:
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
        source = FileSkillsSource("skills/agentic-architecture/SKILL.md")
        return SkillsProvider(source)
    return SkillsProvider(inline_skill())


def build_agent() -> Agent:
    return Agent(
        name="ToolAwareArchitectAdvisor",
        instructions=(
            "You are a data-platform assistant. You have tools — call them "
            "whenever the user asks for the current date or Unity Catalog table "
            "metadata. Follow the loaded SKILL vocabulary. Keep answers concise."
        ),
        client=build_client(),
        tools=[get_today_date, lookup_unity_catalog_table],
        context_providers=[skills_provider()],
    )


async def main() -> None:
    print(
        f"[provider] {os.environ.get('PROVIDER', 'ollama')}  "
        f"[model] {os.environ.get('OLLAMA_MODEL', 'llama3.2')}  "
        f"[skill_mode] {os.environ.get('SKILL_MODE', 'inline')}"
    )
    agent = build_agent()

    # Forces get_today_date tool call.
    q1 = "What is today's date? Use your tools."
    print(f"\n[Q1] {q1}")
    print(f"[A1] {await agent.run(q1)}")

    # Forces lookup_unity_catalog_table tool call.
    q2 = (
        "Look up the table main.sales.events in Unity Catalog "
        "and tell me its columns and storage format."
    )
    print(f"\n[Q2] {q2}")
    print(f"[A2] {await agent.run(q2)}")


if __name__ == "__main__":
    asyncio.run(main())
