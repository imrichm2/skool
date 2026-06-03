# Lab 03 — Tools: Agents That Reach for Real Data

**Module:** 3 — Tools
**Time:** 35 minutes
**File:** `main_tools.py`

---

## What you will do

Run a tool-augmented agent and watch it call functions for live data. Then write a third tool from scratch, register it, and observe the agent use it.

---

## Step 1 — Understand the @tool decorator before you run anything

Open `main_tools.py`. Find the two tool functions:

```python
from agent_framework import tool
from typing import Annotated

@tool
def get_today_date() -> str:
    """Return today's date in ISO 8601 format (YYYY-MM-DD)."""
    return date.today().isoformat()

@tool
def lookup_unity_catalog_table(
    name: Annotated[str, "Fully-qualified table name, e.g. catalog.schema.table"],
) -> str:
    """Look up metadata for a Unity Catalog table and return a JSON summary."""
    ...
```

**Verified API facts** (from reading `agent_framework/_tools.py`):

| What | Actual | Wrong guess |
|---|---|---|
| Decorator name | `@tool` | `@ai_function` (does not exist) |
| Where it lives | `from agent_framework import tool` | — |
| Parameter descriptions | `Annotated[type, "description string"]` | keyword in decorator |
| Tool name source | function `__name__` | must be explicit |
| Tool description source | function docstring | — |
| Return value | any `str`-able value; auto-serialised | must return `Content` |

Now find where the tools are registered:

```python
def build_agent() -> Agent:
    return Agent(
        ...
        tools=[get_today_date, lookup_unity_catalog_table],
        ...
    )
```

`tools=` accepts `FunctionTool` instances, plain callables (auto-wrapped), or a mix.

---

## Step 2 — Run the agent

```bash
OLLAMA_MODEL=qwen3.5:9b python main_tools.py
```

Expected output (exact wording varies):

```
[Q1] What is today's date? Use your tools.
[A1] Today's date is 2026-06-03.

[Q2] Look up the table main.sales.events in Unity Catalog...
[A2] The table `main.sales.events` has the following details:
     Storage Format: Delta
     Columns: id (bigint), event_time (timestamp), payload (string)
```

The agent called `get_today_date()` and returned a date it could not have known from training data. It called `lookup_unity_catalog_table("main.sales.events")` and formatted the JSON response as a readable answer.

---

## Step 3 — Add a third tool

Add this function to `main_tools.py`, before `build_agent()`:

```python
@tool
def list_schema_tables(
    schema: Annotated[str, "Schema name in catalog.schema format, e.g. main.sales"],
) -> str:
    """List all tables registered in a Unity Catalog schema."""
    import json
    catalog, schema_name = (schema.split(".") + [""])[:2]
    tables = [
        {"name": f"{schema}.events",    "format": "delta", "rows": 4_200_000},
        {"name": f"{schema}.customers", "format": "delta", "rows": 180_000},
        {"name": f"{schema}.returns",   "format": "parquet", "rows": 52_000},
    ]
    return json.dumps({"schema": schema, "tables": tables}, indent=2)
```

Register it in `build_agent()`:

```python
tools=[get_today_date, lookup_unity_catalog_table, list_schema_tables],
```

Add a third question to `main()`:

```python
q3 = "What tables exist in the main.sales schema?"
print(f"\n[Q3] {q3}")
print(f"[A3] {await agent.run(q3)}")
```

Run again and verify the agent calls your new tool.

---

## Step 4 — Confirm the tool description matters

Change the docstring of `list_schema_tables` to something vague:

```python
"""Does a thing."""
```

Run again with `q3`. The model may call the wrong tool or not call any tool — the docstring is the only signal the model has about when to use it.

Restore the descriptive docstring before continuing.

---

## Exercise: Tool that can fail

Real tools fail. Add error handling to `lookup_unity_catalog_table` for table names that don't match the expected format:

```python
@tool
def lookup_unity_catalog_table(
    name: Annotated[str, "Fully-qualified table name, e.g. catalog.schema.table"],
) -> str:
    """Look up metadata for a Unity Catalog table and return a JSON summary."""
    parts = name.split(".")
    if len(parts) != 3:
        return f"ERROR: '{name}' is not a valid fully-qualified table name. Expected catalog.schema.table."
    ...
```

Ask the agent: *"Look up the table events in Unity Catalog."* (missing catalog and schema).

Observe: the tool returns the error string, the model reads it, and responds with a helpful correction request rather than crashing.

**Design rule:** Tools should return error strings, not raise exceptions. The model can reason about an error string; it cannot reason about a Python traceback.

---

## Stretch goal: Connect to a real data source

Replace the stub in `lookup_unity_catalog_table` with a real call to a local SQLite database, a REST API, or even a local CSV file. The agent code changes zero lines — only the tool body changes.

---

## Key terms introduced

| Term | Meaning |
|---|---|
| `@tool` | Decorator that wraps a Python function into a `FunctionTool` the agent can call |
| `FunctionTool` | The agent framework's tool wrapper — holds the JSON schema, name, and function |
| `Annotated[type, "desc"]` | Python type hint that carries a description string for the model |
| `tools=` | `Agent` constructor argument that registers tools for the agent to call |
| Tool docstring | The description sent to the model — write it for the model, not for a human |
