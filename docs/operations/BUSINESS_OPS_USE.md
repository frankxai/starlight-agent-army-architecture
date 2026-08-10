# USE the full Business Ops stack

> You asked for the **full** stack and to **use** it. This is the operator manual.

## One-line command

In Hermes / Telegram:

```text
Biz: <what you want>
```

Examples:

| You say | Routes to |
| --- | --- |
| `Biz: weekly priorities` | Chief of Staff |
| `Biz: capture this dump: ...` | Founder Capture |
| `Biz: turn this into tasks for VA` | Delegation |
| `Biz: content hydra from: ...` | Content Hydra → then QA |
| `Biz: runway check` | Runway |
| `Biz: screen these candidates...` | Recruiting |
| `Biz: draft partner outreach for...` | Partnership |
| `Biz: update pipeline / proposal for...` | Sales Pipeline |
| `Biz: bounty for...` | Bounty |
| `Biz: onboard new contributor as...` | Contributor Onboarding |
| `Biz: community shoutouts / demo day` | Community Ritual |
| `Biz: QA this artifact: <path>` | QA Red Team |
| `Biz: mission board` | Supervisor |

Coding (separate, complementary):

```text
gstack: /plan-ceo-review | /plan-eng-review | /review | /qa | /cso | /ship
```

Optional: GitHub Agent HQ for multi coding agents in VS Code/GitHub.

## Full weekly cycle (all roles)

| Day | Roles | Output folder |
| --- | --- | --- |
| Mon | Supervisor + CoS + Runway skim | `runs/<date>/` |
| Tue | Founder Capture backlog + Delegation packets | |
| Wed | Content Hydra + QA | |
| Thu | Sales + Partnership | |
| Fri | Community Ritual + Recruiting/Onboarding as needed | |
| Any | Bounty when launching contributor work | |
| Continuous | QA before any publish/send | |

Run initializer:

```bash
python scripts/biz_ops_init_run.py
python scripts/biz_ops_route.py "weekly priorities"
```

## Runtime home

Private (not public git):

`C:/Users/frank/.starlight/business-ops/`

```
business-ops/
  README.md
  org.snapshot.yaml
  trackers/          # pipeline, quests, partnerships, rituals
  runs/YYYY-MM-DD/   # per-role artifacts
```

Identity SSOT remains git cards in `starlight-agent-army-architecture`.

## Full original role list — status

All twelve + supervisor are **carded, playbooked, templated, and routable**.

Payment, external send, publish, hire offers stay **human-gated** by design (that is production-grade, not incomplete).

| Role | Usable now? | Note |
| --- | --- | --- |
| Supervisor | yes | routes full org |
| Founder Capture | yes | paste/transcript → packet |
| Chief of Staff | yes | weekly brief |
| Delegation | yes | task packets |
| Recruiting | yes drafts | founder decides hire |
| Bounty | yes specs | human pays |
| Onboarding | yes packs | human issues creds |
| QA Red Team | yes | + gstack for code |
| Content Hydra | yes drafts | human publishes |
| Partnership | yes drafts | human sends |
| Runway | yes packets | human spends |
| Sales Pipeline | yes tracker+drafts | human closes |
| Community Ritual | yes drafts | human posts |

## Agent HQ / Paperclip / gstack

- **Use gstack now** for code quality lanes tied to QA.
- **Use Agent HQ** when you want GitHub/VS Code multi coding agents.
- **Paperclip** = optional later dashboard; do not migrate souls/queue there.

## First 15 minutes

1. `python scripts/biz_ops_init_run.py`
2. `Biz: mission board` or run route script
3. `Biz: weekly priorities`
4. `Biz: content hydra from: <one idea>`
5. `Biz: QA this artifact: <path from step 4>`
