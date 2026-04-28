# CI/CD

## Pull request validation
PRs to `main` run:
- checkout
- Python setup
- Databricks CLI setup
- lint
- tests
- forbidden path checks
- bundle validation

## Deployment
- merge to `main` triggers deploy to dev
- test deployment is manual
- prod deployment is manual

## Why this model
- fast feedback in dev
- deliberate promotion to test and prod
- reduced risk of accidental production deployment
