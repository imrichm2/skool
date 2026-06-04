# Task: publish course/labs as a MkDocs Material docs site

You are working inside the `imrichm2/skool` repository (run from the repo root). Goal:
render `course/labs/` as an auto-deploying MkDocs Material site without moving or rewriting
the lab content. Do exactly the steps below, then stop and report.

## 1. Create `mkdocs.yml` at the repo root with this EXACT content

```yaml
site_name: AI Creating AI Agents
site_description: Build, Ground, and Automate Runtime Agents with the Microsoft Agent Framework
site_url: https://imrichm2.github.io/skool/
repo_url: https://github.com/imrichm2/skool
repo_name: imrichm2/skool
edit_uri: edit/main/course/labs/
docs_dir: course/labs

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: teal
      toggle: { icon: material/weather-night, name: Switch to dark mode }
    - scheme: slate
      primary: indigo
      accent: teal
      toggle: { icon: material/weather-sunny, name: Switch to light mode }
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.top
    - content.code.copy
    - search.suggest

nav:
  - Home: index.md
  - "Lab 00 · Setup": 00-setup.md
  - "Lab 01 · Why agents drift": 01-drift.md
  - "Lab 02 · Grounding with SKILL": 02-skill.md
  - "Lab 03 · Tools": 03-tools.md
  - "Lab 04 · Coding agent": 04-coding-agent.md
  - "Lab 05 · Capstone": 05-capstone.md

markdown_extensions:
  - admonition
  - tables
  - pymdownx.highlight: { anchor_linenums: true }
  - pymdownx.superfences
  - toc: { permalink: true }

plugins:
  - search
```

## 2. Create `course/labs/index.md` with this EXACT content

```markdown
# AI Creating AI Agents

**Build, Ground, and Automate Runtime Agents with the Microsoft Agent Framework.**

Most agent tutorials show you how to call an API. This course shows you how to build
agents that build agents — grounded in a versioned SKILL document, equipped with real
tools, and capable of generating a working Runtime Agent in one command.

Every lesson is backed by running Python you execute yourself. No cloud account required —
all labs run locally with Ollama.

## The labs

| # | Lab | Focus |
|---|-----|-------|
| 00 | [Environment setup](00-setup.md) | Get your machine ready |
| 01 | [Why agents drift](01-drift.md) | Run an ungrounded agent |
| 02 | [Grounding with SKILL](02-skill.md) | Add a versioned knowledge source |
| 03 | [Tools](03-tools.md) | Call real functions for live data |
| 04 | [Coding agent](04-coding-agent.md) | An agent that writes agents |
| 05 | [Capstone](05-capstone.md) | Your own SKILL + generated agent |

!!! tip "Work alongside the community"
    Each lab has a discussion thread in the Skool classroom. Post your result when you finish.

> The code these labs run lives in the [repository](https://github.com/imrichm2/skool).
```

## 3. Create `.github/workflows/deploy-docs.yml` with this EXACT content

```yaml
name: deploy-docs
on:
  push:
    branches: [main]
    paths:
      - "course/labs/**"
      - "mkdocs.yml"
      - ".github/workflows/deploy-docs.yml"
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install "mkdocs-material==9.*"
      - run: mkdocs gh-deploy --force
```

## 4. Fix the placeholder clone instructions in `course/labs/00-setup.md`

Make these two exact replacements (and nothing else in that file):

- Replace `git clone https://github.com/<your-repo>/ProjectAgent.git`
  with `git clone https://github.com/imrichm2/skool.git`
- Replace `cd ProjectAgent` with `cd skool`

## 5. Verify locally — this is a hard gate

```bash
pip install "mkdocs-material==9.*"
mkdocs build --strict
```

`mkdocs build --strict` MUST exit 0. Confirm `site/index.html` exists and that
`site/00-setup/`, `site/01-drift/`, `site/02-skill/`, `site/03-tools/`,
`site/04-coding-agent/`, and `site/05-capstone/` were generated. If the build fails,
fix the config you wrote (do NOT alter the lab markdown beyond step 4) and re-run until
it passes. Then delete the local `site/` build artifact so it is not committed.

## 6. Commit and push

```bash
git add mkdocs.yml course/labs/index.md .github/workflows/deploy-docs.yml course/labs/00-setup.md
git commit -m "Add MkDocs Material docs site for labs with auto-deploy"
git push origin main
```

## Guardrails — do NOT

- Do NOT move, rename, or edit any lab file other than the two string fixes in step 4.
- Do NOT touch any `main_*.py`, `requirements.txt`, `SKILL.md`, `README.md`, or `Makefile`.
- Do NOT create or push a `gh-pages` branch by hand — the workflow's `mkdocs gh-deploy`
  produces it on the first run.
- Do NOT add MkDocs plugins or pin a different mkdocs-material major version (keep `9.*`).
- Do NOT commit the `site/` directory.

## After pushing — report back to me

Tell me, in plain text:
1. Confirmation the push succeeded and the `deploy-docs` Action was triggered.
2. The one manual step you cannot perform from git: enabling GitHub Pages in
   **Settings → Pages → Source: Deploy from a branch → branch `gh-pages` / `(root)`**.
3. The resulting site URL: `https://imrichm2.github.io/skool/`.
