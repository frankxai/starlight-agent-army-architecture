# Agent Operating Notes

## Mission

State the repo purpose and current agent objective here.

## Boundaries

- Read scope:
- Write scope:
- Deployment scope:
- Secrets policy: never print or persist raw secrets.

## Verification

Run the smallest reliable set:

```powershell
npm run build
npm test
powershell -ExecutionPolicy Bypass -File scripts/validate-architecture.ps1
```

## Handoff

Every agent handoff should include:

- Files changed
- Tests run
- Decisions made
- Open risks
- Next command to continue
