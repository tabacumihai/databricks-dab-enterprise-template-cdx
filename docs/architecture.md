# Architecture

## Goal
This repository provides a standard deployment model for Databricks projects using Databricks Asset Bundles and GitHub Actions.

## Layers

### Source layer
- notebooks
- Python modules
- tests
- documentation

### Deployment layer
- databricks.yml
- resources/

### Delivery layer
- .github/workflows/

## Principles
- all deployable resources live in code
- environments are separated by target
- business logic is reusable
- CI validates before deploy
- production promotion is gated

## Collaboration
If another Databricks engineer joins the project:
- they create a feature branch
- work in notebooks/resources/src/tests
- open a PR
- receive review through CODEOWNERS
- merge only after passing checks
