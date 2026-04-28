# Branching and release

## Recommended branching model
- `main`
- `feature/*`
- `bugfix/*`
- `hotfix/*`

## Release model
- merge to `main` deploys to `dev`
- `test` deployment is manual
- `prod` deployment is manual and should require environment approvals

## Why this works
This model keeps one source of truth for code while still allowing controlled promotion across workspaces.

## Release checklist
1. PR approved
2. All validation checks pass
3. Deploy to dev succeeds
4. Smoke tests in dev pass
5. Promote to test
6. Promote to prod only after business and engineering approval
