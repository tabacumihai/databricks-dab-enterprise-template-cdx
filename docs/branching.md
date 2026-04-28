# Branching

## Daily development
Every change should start from a fresh branch created from `main`.

Examples:
- `feature/add-order-ingestion`
- `bugfix/fix-null-check`
- `hotfix/prod-alert-threshold`

## Rules
- never push directly to `main`
- keep branches short-lived
- rebase or merge from `main` frequently if the branch lives for several days
- prefer small PRs over large ones
