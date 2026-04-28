# Enterprise template reference

This file exists because many teams keep both a short `README.md` and a longer design-oriented document.

## When to read this file

Read this file when you want the reasoning behind the structure, not just the quick-start.

## Design goals

- standardize Databricks repository structure
- reduce onboarding time for new engineers
- support many future jobs, dashboards, and pipelines
- keep CI/CD rules reusable across projects
- encourage code reuse through `src/`

## Why this structure works

### It separates concerns cleanly
- deployment config in `databricks.yml`
- Databricks resources in `resources/`
- execution code in `notebooks/`
- reusable Python in `src/`
- tests in `tests/`
- delivery automation in `.github/`
- project guidance in `docs/`

### It scales with multiple engineers
A new engineer should be able to:
1. clone the repo
2. read `docs/onboarding.md`
3. work in a feature branch
4. add a notebook or job
5. open a PR
6. rely on CI and reviewers before merge

## What should remain stable

These should remain mostly stable across projects:
- repository root structure
- `.github/workflows/`
- `.github/CODEOWNERS`
- `docs/`
- separation between `resources/`, `notebooks/`, and `src/`

## What teams usually customize per project

- bundle name
- workspace URLs
- catalog/schema names
- warehouse IDs
- owner emails
- service principal IDs
- notebook names
- job definitions
- dashboard assets
- pipeline logic
- runtime dependencies

## Recommended engineering model

- keep notebooks thin
- keep business logic in Python modules
- write tests for shared Python logic
- use one deployable `main` branch
- use environment secrets for credentials
- use CODEOWNERS and protected branches
- use target promotion instead of code duplication

## Future-proofing

This template is ready to evolve into:
- multiple domains under one repo
- agentic/AI helpers in `src/platform_core/ai/`
- wheel packaging
- shared data quality modules
- reusable dashboard refresh jobs
- additional Databricks resources as needed
