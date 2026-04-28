# Databricks project bootstrap checklist

## Phase 1 — Clone and local setup
1. Clone the repository
2. Create a virtual environment
3. Install `requirements-dev.txt`
4. Copy `.databrickscfg.example` to a local `.databrickscfg`
5. Replace placeholder values in `databricks.yml` and `config/*.yml`

## Phase 2 — Configure Databricks access
1. Create a PAT or use the approved auth method
2. Set local auth for development
3. Confirm `databricks version`
4. Run `databricks bundle validate -t dev`

## Phase 3 — Configure GitHub
1. Protect `main`
2. Configure CODEOWNERS
3. Create `dev`, `test`, and `prod` environments
4. Add `DATABRICKS_HOST` and `DATABRICKS_TOKEN` secrets per environment

## Phase 4 — Create the first feature branch
1. Create `feature/<name>`
2. Make a small change
3. Add or update tests
4. Push branch and open PR

## Phase 5 — PR flow
1. CI runs lint, tests, and bundle validation
2. CODEOWNERS review
3. Required approvals are collected
4. Merge into `main`

## Phase 6 — Dev deployment
1. Merge to `main`
2. `deploy-dev` runs automatically
3. Verify Databricks resources in the dev workspace
4. Run smoke tests

## Phase 7 — Test and prod promotion
1. Trigger `deploy-test`
2. Validate in test
3. Trigger `deploy-prod`
4. Validate in prod

## Phase 8 — Ongoing engineering rules
### Do
- use feature branches
- keep notebooks thin
- keep reusable logic in `src/`
- write tests for shared logic
- update docs when introducing new patterns

### Do not
- commit secrets
- edit managed jobs manually in the UI
- bypass PR review
- change repo structure casually
