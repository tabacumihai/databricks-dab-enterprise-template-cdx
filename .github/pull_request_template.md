## Summary
Describe the change clearly and concisely.

## Why
Explain the reason for the change and the problem it solves.

## Scope
- [ ] Source code only
- [ ] Databricks job change
- [ ] Databricks pipeline change
- [ ] Dashboard change
- [ ] CI/CD workflow change
- [ ] Documentation change

## Databricks impact
- [ ] New notebook added
- [ ] Existing notebook changed
- [ ] New job added
- [ ] Existing job changed
- [ ] New pipeline added
- [ ] Existing pipeline changed
- [ ] New dashboard added
- [ ] Existing dashboard changed
- [ ] No Databricks resource impact

## Validation performed
- [ ] Unit tests passed locally
- [ ] `ruff check .` passed
- [ ] `black --check .` passed
- [ ] `yamllint .` passed
- [ ] `databricks bundle validate -t dev` passed
- [ ] Manual smoke test completed if required

## Deployment notes
Describe any post-deploy checks, manual follow-up, or operational considerations.

## Rollback plan
Explain how this change can be reverted if needed.