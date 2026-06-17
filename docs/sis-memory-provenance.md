# SIS Memory And Provenance

SIS is the Starlight substrate for remembering decisions and proving how work happened.

## What To Store

| Store | Examples |
| --- | --- |
| Decisions | ADRs, tradeoffs, accepted/rejected alternatives |
| Sources | Official docs, GitHub repos, issues, deployment logs |
| Health | `/heart`, audit summaries, yellow/red items |
| Handoffs | Who/what did what, files changed, tests run |
| Capabilities | Which agent/profile can read, write, deploy, or message |

## What Not To Store

- Raw API keys
- Session tokens
- Private customer data unless explicitly approved
- Unreviewed model output as fact
- Chat messages that contain credentials

## Provenance Record Shape

```json
{
  "id": "decision-2026-06-17-agent-os",
  "type": "architecture-decision",
  "actor": "codex",
  "repo": "starlight-agent-army-architecture",
  "sources": [
    "https://docs.openclaw.ai/",
    "https://docs.langchain.com/oss/python/deepagents/overview"
  ],
  "decision": "Use OpenClaw as gateway and Codex as repo control plane.",
  "verification": ["scripts/validate-architecture.ps1"],
  "risk": "Gateway requires owner/auth setup before public use."
}
```

## Memory Quality Bar

A useful memory entry should answer:

- What changed?
- Why?
- Based on which source?
- How was it verified?
- What remains risky?
