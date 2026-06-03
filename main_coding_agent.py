"""
Coding Agent — reads a SKILL and emits a Runtime Agent Python script.

This is Layer 3 of the "AI Creating AI Agents" workshop.

ROLE (per SKILL vocabulary):
  Coding Agent = build-time agent that reads a SKILL and emits artifacts.
  It does NOT serve end users. The emitted script IS the Runtime Agent.

WHAT IT DOES:
  1. Reads the SKILL file at the path you provide (or SKILL.md by default).
  2. Decides which tools the Runtime Agent should expose based on the SKILL's
     domain (or uses the stubs provided if the SKILL doesn't specify tools).
  3. Calls write_agent_file() with a complete, runnable main_<name>.py.

NOTE ON PRODUCTION:
  For anything touching regulated data, wrap this in a Workflow (human-in-the-
  loop + checkpoint). A bare Coding Agent is fine for dev/workshop use.

API VERIFIED from installed agent_framework source:
  - @tool decorator (agent_framework._tools, re-exported at top level)
  - Agent(tools=[...], context_providers=[...], instructions=..., client=...)
  - No @ai_function — that symbol does not exist in this package.

Run:
  # Default skill (SKILL.md in this directory):
  OLLAMA_MODEL=qwen3.5:9b .venv/bin/python main_coding_agent.py

  # Custom skill file:
  OLLAMA_MODEL=qwen3.5:9b .venv/bin/python main_coding_agent.py path/to/SKILL.md

  # Dry-run (print generated code, don't write file):
  OLLAMA_MODEL=qwen3.5:9b .venv/bin/python main_coding_agent.py --dry-run
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from typing import Annotated

from agent_framework import Agent, tool

# ---------------------------------------------------------------------------
# Provider (same swap logic as the rest of the project)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Tools the Coding Agent can call
# ---------------------------------------------------------------------------

@tool
def read_skill_file(
    path: Annotated[str, "Path to the SKILL.md file to read"],
) -> str:
    """Read a SKILL file from disk and return its full contents."""
    skill_path = Path(path)
    if not skill_path.exists():
        return f"ERROR: file not found: {path}"
    return skill_path.read_text(encoding="utf-8")


@tool
def write_agent_file(
    filename: Annotated[str, "Output filename, e.g. main_myskill.py"],
    content: Annotated[str, "Complete Python source code for the Runtime Agent"],
) -> str:
    """Validate syntax then write the Runtime Agent script to generated/."""
    import ast

    try:
        ast.parse(content)
    except SyntaxError as exc:
        return (
            f"SYNTAX ERROR at line {exc.lineno}: {exc.msg}\n"
            "Fix the code — remove stray triple-quoted strings and bare "
            "string literals outside any function — then call write_agent_file again."
        )

    out_dir = Path(__file__).parent / "generated"
    out_dir.mkdir(exist_ok=True)
    safe_name = Path(filename).name
    if not safe_name.endswith(".py"):
        safe_name += ".py"
    out_path = out_dir / safe_name
    out_path.write_text(content, encoding="utf-8")
    return f"Written {len(content)} chars to {out_path}"


# ---------------------------------------------------------------------------
# Meta-SKILL: what the Coding Agent knows about the target framework
#
# This is the key grounding that prevents hallucinated API names.
# Every line here was verified by reading the installed package source.
# ---------------------------------------------------------------------------

META_SKILL = """\
You are a Coding Agent.  Your ONLY job is:
  1. Call read_skill_file() with the path I give you.
  2. Read the SKILL frontmatter to extract the `name:` field.
  3. Generate a complete, runnable Python Runtime Agent script.
  4. Call write_agent_file(filename="main_<name>.py", content=<script>).

=== VERIFIED API — copy these patterns exactly, do not invent alternatives ===

--- TOP OF FILE (always include these exact imports) ---
import os
import asyncio
from typing import Annotated
from agent_framework import Agent, InlineSkill, SkillFrontmatter, SkillsProvider, tool


--- build_client() — copy this function verbatim every time ---
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


--- @tool decorator — use with no arguments; Annotated for param descriptions ---
@tool
def my_tool(param: Annotated[str, "what this param is"]) -> str:
    'Docstring becomes the tool description.'
    return "result string"


--- Agent construction — tools= and context_providers= are keyword-only ---
agent = Agent(
    name="MyAgent",
    instructions="system prompt",
    client=build_client(),
    tools=[tool1, tool2],
    context_providers=[skills_provider()],
)


--- Skill grounding ---
IMPORTANT: in the generated file, write multi-line string values using
parenthesised single-quoted segments, NOT triple-quoted strings.
That avoids syntax errors from stray quote runs.

def skills_provider() -> SkillsProvider:
    skill = InlineSkill(
        frontmatter=SkillFrontmatter(name="...", description="..."),
        instructions=(
            "First rule. "
            "Second rule. "
            "Third rule."
        ),
    )
    return SkillsProvider(skill)


--- Running the agent — AgentResponse.__str__ returns the text ---
result = await agent.run("user message")
print(result)


=== REQUIRED STRUCTURE OF THE EMITTED SCRIPT ===

Section 1: Module docstring naming the skill and the run command
Section 2: Imports (exactly as shown above)
Section 3: build_client() copied verbatim from the template above
Section 4: 1-3 @tool functions suited to the SKILL domain
Section 5: skills_provider() embedding the SKILL name, description, and
           instructions from the file you read
Section 6: build_agent() wiring client + tools + context_providers
Section 7: async main() — MUST start with "agent = build_agent()" on its own line,
           then run 2 example prompts and print results.
           Use ONLY "await agent.run(...)" — no other run method exists.
           Do NOT use triple-quoted strings anywhere in main() or anywhere else
           in the generated file except the module-level docstring on line 1.
Section 8: if __name__ == "__main__": asyncio.run(main())

Return ONLY raw Python source — no markdown fences, no prose outside the file.
The file must be runnable with:
    OLLAMA_MODEL=qwen3.5:9b .venv/bin/python generated/main_<name>.py
"""


# ---------------------------------------------------------------------------
# Coding Agent
# ---------------------------------------------------------------------------

def build_coding_agent() -> Agent:
    return Agent(
        name="CodingAgent",
        instructions=META_SKILL,
        client=build_client(),
        tools=[read_skill_file, write_agent_file],
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main(skill_path: str, dry_run: bool) -> None:
    provider = os.environ.get("PROVIDER", "ollama")
    model = os.environ.get("OLLAMA_MODEL", "llama3.2")
    print(f"[coding-agent] provider={provider}  model={model}")
    print(f"[coding-agent] skill={skill_path}  dry_run={dry_run}")

    agent = build_coding_agent()

    if dry_run:
        # Replace write_agent_file with a version that only prints
        from agent_framework import tool as tool_decorator

        @tool_decorator
        def write_agent_file(  # noqa: F811  (intentional shadow for dry-run)
            filename: Annotated[str, "Output filename"],
            content: Annotated[str, "Python source code"],
        ) -> str:
            """Dry-run: print the generated script instead of writing it."""
            print(f"\n{'='*60}")
            print(f"DRY-RUN: would write {filename}")
            print(f"{'='*60}")
            print(content)
            print(f"{'='*60}\n")
            return f"DRY-RUN: {len(content)} chars (not written)"

        agent_tools = [read_skill_file, write_agent_file]
        prompt = (
            f"The SKILL file is at: {skill_path}\n"
            "Read it with read_skill_file, then generate and write the Runtime "
            "Agent script using write_agent_file."
        )
        result = await agent.run(prompt, tools=agent_tools)
    else:
        prompt = (
            f"The SKILL file is at: {skill_path}\n"
            "Read it with read_skill_file, then generate and write the Runtime "
            "Agent script using write_agent_file."
        )
        result = await agent.run(prompt)

    print(f"\n[coding-agent] done.\n{result}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coding Agent: SKILL → Runtime Agent script")
    parser.add_argument(
        "skill_path",
        nargs="?",
        default="SKILL.md",
        help="Path to the SKILL.md file (default: SKILL.md)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated code instead of writing to disk",
    )
    args = parser.parse_args()
    asyncio.run(main(skill_path=args.skill_path, dry_run=args.dry_run))
