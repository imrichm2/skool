"""
Zero-Azure Runtime Agent — runs on your Ubuntu box with no cloud setup.

Default provider is OLLAMA (fully local). Set PROVIDER=openai to use OpenAI
instead. Same Agent class as main.py — only the client line changes, which is
the whole point of Agent Framework's provider-agnostic design.

Verified against the live packages (April 2026):
  - agent_framework.ollama.OllamaChatClient   (beta package: install with --pre)
  - agent_framework.openai.OpenAIChatClient   (released)
  - constructor args confirmed: OllamaChatClient(host=, model=),
    OpenAIChatClient(model, api_key=)

----------------------------------------------------------------------
OLLAMA path (default) — on your Ubuntu server:
  1. curl -fsSL https://ollama.com/install.sh | sh
  2. ollama pull llama3.2          # or any model you like
  3. pip install --pre agent-framework-ollama        # beta -> needs --pre
     pip install agent-framework-core
  4. python main_local.py

OPENAI path:
  1. pip install agent-framework-openai agent-framework-core
  2. export PROVIDER=openai
     export OPENAI_API_KEY=sk-...
     export OPENAI_MODEL=gpt-4.1   # optional, defaults below
  3. python main_local.py
----------------------------------------------------------------------
"""

import os
import asyncio

from agent_framework import Agent


def build_client():
    provider = os.environ.get("PROVIDER", "ollama").lower()

    if provider == "openai":
        from agent_framework.openai import OpenAIChatClient
        return OpenAIChatClient(
            model=os.environ.get("OPENAI_MODEL", "gpt-4.1"),
            api_key=os.environ["OPENAI_API_KEY"],  # raises clearly if unset
        )

    # default: fully local Ollama
    from agent_framework.ollama import OllamaChatClient
    return OllamaChatClient(
        host=os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
        model=os.environ.get("OLLAMA_MODEL", "llama3.2"),
    )


def build_agent() -> Agent:
    return Agent(
        name="HelloLocalAgent",
        instructions=(
            "You are a concise data-platform assistant. "
            "Answer in at most three sentences. If unsure, say so."
        ),
        client=build_client(),
    )


async def main() -> None:
    print(f"[provider] {os.environ.get('PROVIDER', 'ollama')}")
    agent = build_agent()

    result = await agent.run("In one line: what is the medallion architecture?")
    print("\n[run]    ", result)

    print("\n[stream] ", end="", flush=True)
    async for update in agent.run(
        "Name three reasons to keep build-time and runtime agents separate.",
        stream=True,
    ):
        print(update.text or "", end="", flush=True)
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())