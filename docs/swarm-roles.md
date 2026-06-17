# Swarm Roles

| Role | Runtime | Inputs | Outputs | Guardrails |
| --- | --- | --- | --- | --- |
| Founder operator | Human | Goals, constraints, acceptance criteria | Mission brief | Owns priority and approval |
| Control plane | Codex | Repo, tests, docs, issues | Commits, PRs, guides | Uses clean worktrees for WIP repos |
| Local worker | Hermes Agent | Kanban cards, repo snippets, MCP tools | Handoffs, task updates | Scoped profile identity |
| Gateway operator | OpenClaw | Chat/channel messages | Routed sessions | Allowlist channels and users |
| Harness runner | DeepAgents | Research briefs, code tasks | Reports, plans, artifacts | Human-in-the-loop for side effects |
| Maintainer lane | Claude Code | CLAUDE.md, skills, subagents | Code/docs changes | Repo-specific rules |
| Memory/provenance | SIS | Events, decisions, health | Audit trails, recall, heart checks | No raw secrets |

The core operating rule: every worker needs an identity, scope, review boundary, and exit condition.
