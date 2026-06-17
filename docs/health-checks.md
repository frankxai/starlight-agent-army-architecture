# Health Checks

Run health checks before handing work to an agent swarm and before any deploy.

## Local Commands

```powershell
powershell -ExecutionPolicy Bypass -File scripts/validate-architecture.ps1
powershell -ExecutionPolicy Bypass -File ..\agentic-architecture-field-guide\scripts\agent-os-audit.ps1
```

## Expected Signals

| Signal | Healthy |
| --- | --- |
| Hermes Agent | `hermes version` returns a version |
| Hermes dashboard | `http://127.0.0.1:9119/sessions` returns HTTP 200 |
| OpenClaw | `openclaw --version` returns a version |
| OpenClaw gateway | Dashboard/status responds on loopback or configured host |
| DeepAgents | Python import succeeds |
| Deep Agents Code | `dcode --version` returns a version |
| Codex | `codex --version` returns a version |
| Claude Code | `claude --version` returns a version |
| MCP Doctor | `mcp-doctor audit --quick` runs |
| SIS | `/heart` is non-red |

## Yellow Is Acceptable When

- A dashboard is intentionally stopped.
- A cloud CLI is not needed for the current task.
- A remote MCP server is skipped in quick mode.
- A private optional subsystem is absent from a public checkout.

## Red Means Stop

- Repo worktree contains unrelated unreviewed edits.
- Secrets appear in logs, memory, docs, or commits.
- Gateway is public without owner/auth policy.
- Deploy target is unknown.
- Tests fail on a code path the agent touched.
