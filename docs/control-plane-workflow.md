# Control-Plane Workflow

## Mission Intake

Capture:

- Goal and non-goals
- Repos in scope
- Data/tool permissions
- Deployment target
- Verification commands
- Rollback or defer conditions

## Execution

1. Inspect repo status before edits.
2. If a repo is dirty or ahead with unrelated work, use a clean worktree from `origin/main`.
3. Assign Hermes or DeepAgents lanes only after the repo boundary is clear.
4. Keep OpenClaw routing read-mostly unless an operator explicitly approves side effects.
5. Run local validators, tests, and health probes.
6. Commit only focused changes.
7. Push to the agreed target branch.
8. Record provenance and remaining yellow items in SIS.

## Deploy Targets

| Target | Use | Avoid |
| --- | --- | --- |
| Vercel | Web dashboards, docs, APIs, cron, workflows | Long-running gateways |
| Railway | Always-on gateway/process services | Static-only docs |
| Cloudflare | Edge APIs, Workers, static sites, Durable Objects | Heavy local tool execution |
| Local machine | Private repos, agent cockpit, personal tools | Public unauthenticated access |
