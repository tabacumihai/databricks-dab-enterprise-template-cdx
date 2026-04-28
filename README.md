# databricks-dab-enterprise-template

Enterprise-ready Databricks Asset Bundles template for Azure Databricks projects.

## Purpose

This repository is a reusable template for Databricks projects that need:

- source-controlled Databricks resources
- pull request based development
- GitHub Actions CI/CD
- dev / test / prod deployment targets
- reusable jobs, dashboards, and pipelines
- onboarding documentation for multiple engineers

## Repository structure

### `databricks.yml`
Root bundle configuration. This is the main entry point for Databricks Asset Bundles.

### `config/`
Reference environment configuration files. These are primarily documentation and local helper values, not secret stores.

### `docs/`
Documentation for architecture, CI/CD, branching, onboarding, and operations.

### `resources/`
Databricks resources deployed by the bundle:
- jobs
- pipelines
- dashboards
- permissions
- compute templates

### `notebooks/`
Notebook entrypoints used by jobs and pipelines.

### `src/`
Reusable Python logic. Keep notebooks thin and move reusable logic here.

### `tests/`
Local and CI test coverage for Python modules.

### `.github/`
Review workflow, CODEOWNERS, PR template, and deployment pipelines.

## Branching strategy

Use a single deployable `main` branch and short-lived feature branches:

- `feature/<name>`
- `bugfix/<name>`
- `hotfix/<name>`

Flow:

1. Create feature branch
2. Open PR into `main`
3. CI validates code and bundle
4. CODEOWNERS review and approve
5. Merge to `main`
6. Auto-deploy to `dev`
7. Manually promote to `test`
8. Manually promote to `prod`

## Why one `main` branch

This reduces drift between environments. The same code is promoted through environments, while target-specific settings are handled by bundle targets and GitHub environment secrets.

## Local setup

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Validate locally

```bash
pytest
databricks bundle validate -t dev
```

## GitHub setup

### Branch protection
Protect `main`:
- require PR before merge
- require approvals
- require CODEOWNERS review
- require passing checks
- block direct pushes
- block force pushes

### Environments
Create:
- `dev`
- `test`
- `prod`

Add secrets per environment:
- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

Recommended reviewers:
- dev: optional
- test: 1 reviewer
- prod: 2 reviewers

## Databricks setup

Replace placeholders in:
- `databricks.yml`
- `config/*.yml`
- `resources/*.yml`

You should update:
- workspace host URLs
- warehouse IDs
- owner emails
- service principal ID
- group names
- cluster node types
- spark versions

## How to add new functionality

### Add a new notebook
Place it in `notebooks/` under the right subfolder.

### Add a new job
Create a new YAML file in `resources/jobs/`.

### Add a new dashboard
Add resource definition in `resources/dashboards/` and commit the dashboard JSON.

### Add a new DLT / pipeline
Create or update files under `resources/pipelines/` and `notebooks/dlt/`.

### Add Python libraries
- Add runtime libraries to `requirements.txt`
- Add dev tools to `requirements-dev.txt`
- If the Python package itself changes, update `pyproject.toml`

### Add AI / agents
Recommended structure:
- `src/platform_core/ai/` for reusable AI logic
- add necessary packages to `requirements.txt`
- keep secrets external, never hardcode tokens

## Commands

```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev
databricks bundle deploy -t test
databricks bundle deploy -t prod
databricks bundle summary -t dev
pytest
ruff check .
black --check .
```

## Operating principles

- No manual Databricks UI edits for managed resources
- Everything deployable must live in source control
- Notebooks should be thin wrappers
- Business logic should be reusable in `src/`
- CI should validate before deploy
- Promotion should use the same code across environments
