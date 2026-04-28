# GitHub Repository Settings

This file documents the GitHub settings that must be configured manually for this repository.

---

## 1. Default branch

Set the default branch to:

- `main`

---

## 2. Branch protection / ruleset for `main`

Configure a branch protection rule or repository ruleset for `main` with the following requirements:

- Require a pull request before merging
- Require at least 1 approval for non-production changes
- Require at least 2 approvals if your team wants stricter production governance
- Require review from Code Owners
- Require status checks to pass before merging
- Dismiss stale approvals when new commits are pushed
- Block direct pushes to `main`
- Block force pushes
- Optionally require conversation resolution before merge

Recommended required checks:
- `validate / validate`

If you split validation into multiple jobs later, list all required job names explicitly.

---

## 3. GitHub environments

Create the following environments:

- `dev`
- `test`
- `prod`

### Secrets to define in each environment

- `DATABRICKS_HOST`
- `DATABRICKS_TOKEN`

### Recommended reviewers

- `dev`: optional reviewers
- `test`: 1 required reviewer
- `prod`: 2 required reviewers

### Why environment secrets

Environment secrets ensure that:
- only workflows targeting that environment can access those secrets
- approval gates can protect access to deployment credentials

---

## 4. Actions permissions

At the repository level, allow GitHub Actions and reusable workflows required by this repository.

If your organization restricts third-party actions, explicitly allow:
- `actions/checkout`
- `actions/setup-python`
- `databricks/setup-cli`

---

## 5. CODEOWNERS expectations

Ensure that all teams referenced in `.github/CODEOWNERS`:
- exist in the GitHub organization
- have access to this repository

---

## 6. Optional enhancements

Depending on your governance model, consider enabling:
- merge queue
- signed commits
- secret scanning
- Dependabot alerts
- custom deployment protection rules for production