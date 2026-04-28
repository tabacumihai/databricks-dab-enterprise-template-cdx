# Onboarding

## What to install
- Python 3.11+
- Databricks CLI
- Git
- VS Code or preferred editor

## First steps
1. Clone repository
2. Create virtual environment
3. Install dev dependencies
4. Copy `.databrickscfg.example` to local `.databrickscfg` if needed
5. Run tests
6. Run `databricks bundle validate -t dev`

## Where to make changes
- new notebook logic: `notebooks/`
- reusable Python: `src/`
- new Databricks jobs: `resources/jobs/`
- dashboards: `resources/dashboards/`
- DLT: `resources/pipelines/`
