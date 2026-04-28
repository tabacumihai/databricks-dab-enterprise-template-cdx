# Operations

## Ownership
Each deployed bundle should have a clear owner email and, in production, ideally a service principal run identity.

## Monitoring
At minimum, monitor:
- failed workflow runs
- failed Databricks jobs
- delayed scheduled tasks
- unexpected schema changes

## Recovery
Prefer rollback through version control and redeployment instead of manual edits in the Databricks UI.
