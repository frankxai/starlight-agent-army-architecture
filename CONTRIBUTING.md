# Contributing

This repo is Starlight-specific. Put neutral ecosystem material in the field guide or awesome list.

## Standards

- Keep upstream ownership clear.
- Include trust boundaries for every new role/config.
- Add validation steps for every new template.
- Never add real secrets.
- Prefer small, composable examples over giant all-in-one configs.

## Local Check

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate-architecture.ps1
```
