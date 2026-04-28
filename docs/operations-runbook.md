# Operations runbook

## Validate locally
```bash
pytest
ruff check .
black --check .
yamllint .
databricks bundle validate -t dev
```

## Deploy to dev
Merge an approved PR to `main`.

## Deploy to test
Run workflow `deploy-test`.

## Deploy to prod
Run workflow `deploy-prod`.

## Rollback
Revert the bad commit on `main` and redeploy the target.

## Emergency changes
Use `hotfix/*` branch and standard PR flow.
