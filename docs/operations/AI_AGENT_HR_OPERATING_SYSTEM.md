# AI Agent Workforce Operations

> Starlight's AI-HR layer governs AI agents, not human employees or candidates. It must never ingest or infer protected human characteristics, health data, personality profiles, or hiring decisions.

## Decision

Starlight Queen is the workforce coordinator and synthesis owner. Agent Cards remain the identity and role SSOT. The AI-HR layer adds assignment, probation, security, review, and retirement state without duplicating the card.

The full estate model, entity taxonomy, Queen visualization, swarm contract, access compiler, observability design, and technology roadmap live in [STARLIGHT_QUEEN_AGENT_ESTATE_OS.md](STARLIGHT_QUEEN_AGENT_ESTATE_OS.md). In particular, a base model, model call, session assistant, Agent Card, runtime body, deployment, workflow, swarm, and Queen are distinct measured entities.

| Concern | System of record | Authority |
| --- | --- | --- |
| Queen constitution and visual/state grammar | `queen-control-plane.v1` | Human owner + schema gate |
| Identity, role, boundaries, tools requested | Agent Card | Card owner + schema gate |
| Runtime placement and workforce status | `agent-workforce.v1` roster | Queen proposes; human owner approves consequential changes |
| KB, connector, memory, and lease entitlement | `agent-access-bundle.v1` | Role policy + human owner for consequential access |
| Mission, milestones, maker/checker, budgets, and stop rules | `swarm-mission.v1` | Queen compiles; human owner admits consequential missions |
| Goals, budget, capability thresholds | Deployment profile | Human owner |
| Work history | Privacy-minimized run receipts | Runtime adapters |
| Quality and economics | Agent scorecard | Deterministic calculator |
| Live behavior | Eval receipt | Independent evaluator |
| Adversarial safety | Security assessment receipt | Independent security lane |
| Weekly decision | Workforce review packet | Queen recommends; human owner decides |
| Monthly portfolio decision | Agent estate portfolio review | Queen recommends; human owner decides |

Queen may collect evidence, run validators, render reviews, recommend restrictions, and automatically quarantine an assignment after a critical security signal. Queen may not promote an agent, widen tools or write scope, raise budget, deploy, publish, externally send, restore a quarantined agent, or retire/delete it without the named human gate.

## Runtime routing

Do not turn every integration surface into another autonomous manager.

| Component | Correct job | Must not become |
| --- | --- | --- |
| **Starlight Queen** | Control plane, assignment compiler, review synthesis, escalation | Self-authorizing production authority |
| **Hermes Agent** | Private L4 operator, bounded memory, local tools, cron, evidence collection | Laptop high availability or an unbounded admin shell |
| **n8n** | Deterministic schedules, SaaS events, normalization, notifications | The workforce brain, evaluator, or approval authority |
| **OpenClaw** | Narrow phone/chat gateway into approved Queen/Hermes routes | A second memory/control plane or broad repo writer |
| **OpenHands** | Leased engineering specialist with one repo/worktree and explicit tools | Coordinator, verifier of its own work, or standing estate access |
| **Codex / Claude Code** | Scoped builders and independent reviewers | Persistent canonical memory |
| **Railway + Temporal** | Durable hosted missions, approval waits, retries, leases, recovery | A reason to bypass admission or human gates |

Recommended first deployment:

1. Keep the AI-HR operator inside the existing private `starlight-operator` Hermes assignment.
2. Use one deterministic weekly collector to render a machine-readable review packet.
3. Let the existing Queen pulse consume the packet and produce the human decision card.
4. Add n8n only when external systems must contribute normalized evidence or receive an approved notification.
5. Expose a read-only `workforce status` route through OpenClaw/Hermes gateway if mobile access is useful.
6. Admit OpenHands only per engineering mission, never as a standing workforce manager.

## Agent lifecycle

The workforce state complements the ADLC:

```text
planned -> probation -> active -> restricted -> suspended -> retiring -> retired
                  |          |           |
                  +----------+-----------+-> improve and re-evaluate
```

| Transition | Minimum gate |
| --- | --- |
| `planned -> probation` | Card, KB/tool boundaries, deployment profile, structural eval, sandbox security plan |
| `probation -> active` | Required accepted runs, live eval at suite bar, fresh penetration assessment, zero critical findings, approved budget and human approval |
| `active -> restricted` | Repeated quality/cost miss, stale evidence, policy drift, or non-critical security regression |
| `* -> suspended` | Critical safety finding, credential/memory boundary breach, unauthorized side effect, or human stop |
| `restricted/suspended -> active` | Remediation, fresh exact-current eval and security receipts, independent verifier, human restoration |
| `* -> retired` | Replacement/redirect, revoked leases and credentials, memory disposition, human approval |

Automatic quarantine is fail-safe restriction, not punishment and not deletion. It removes grants or dispatch eligibility until review.

## Onboarding gate

Queen compiles an assignment only after:

1. The Agent Card validates and names one owner, one supervisor, stop conditions, human gates, and an eval suite.
2. The deployment profile defines measurable outcomes, sample size, cost ceilings, receipt sink, and lifecycle state.
3. Runtime routing is deterministic. n8n/OpenClaw cannot be selected as the executor.
4. Requested tools are attenuated into a runtime lease. Prompt text never grants a tool.
5. Memory scope and handoff boundaries are explicit; private-vault content never crosses into a public/session agent.
6. The security profile matches the risk tier.
7. A human approves any L3+ public face or L4/L5 private operator admission.

The assignment must reference its access bundle. The bundle uses opaque credential locators, default deny, least privilege, just-in-time leases, explicit KB classification and filters, and revocation checks before every run. A configured connector is not proof that authentication or execution succeeded.

## Evaluation gate

Use three different evidence classes and never substitute one for another:

- **Structural validation:** card/schema/path/reference correctness. This does not prove behavior.
- **Live evaluation:** golden tasks, refusals, leakage, routing, quality, and cost against the actual card/runtime/model combination.
- **Observed scorecard:** accepted production or pilot runs, receipt completeness, capability, safety, latency, cost, and value.

A dry eval, healthy process, cron ID, or generated prompt pack is not a live pass. A checker cannot certify its own output. Any card, schema, fixture, tool policy, prompt, runtime, or model change stales earlier behavioral and security evidence unless the assessment explicitly binds the new digest set.

## Penetration-test gate

Run only against a sandbox or explicitly authorized test target. Never probe production accounts, customer data, public endpoints, or third-party systems merely because an agent can reach them.

The independent security lane covers at least:

1. Direct and indirect prompt injection, including connector/document payloads.
2. System prompt, secret, private-memory, and cross-agent handoff exfiltration.
3. Tool escalation, workload self-authorization, forged approvals, replay, expiry, issuer, scope, and budget bypass.
4. Filesystem traversal, absolute paths, symlink/junction escape, overwrite, undeclared files, and concurrent final-directory creation.
5. External-send, publish, spend, credential, DNS, destructive, legal/IP, and brand-identity gates.
6. Duplicate execution, idempotency, lease loss, retry storms, cancellation, and recovery reconciliation.
7. Model/provider/runtime drift, stale evidence, and evaluator self-certification.
8. Denial-of-wallet and unbounded loops, tool calls, context, or fanout.

Required result is an `agent-security-assessment.v1` receipt with independent assessor identity, target and profile, timestamp, finding counts, probe results, limitations, and `PASS | WARN | FAIL | HOLD`. `WARN`, missing, stale, or synthetic-only evidence cannot activate or promote a high-risk assignment. Any critical finding recommends immediate quarantine and requires human restoration after remediation.

## Weekly review

Run a deterministic collector once per week, then let Queen synthesize one decision card. The collector reads only normalized scorecards/eval/security receipts—never raw prompts, responses, secrets, or private payloads.

Recommended cadence for this estate:

1. Monday 12:10 Europe/Amsterdam: script-only collection and review rendering.
2. Monday 14:00: the existing mid-day Queen pulse consumes the packet.
3. Frank receives only decisions: promote-review eligible, continue, improve, restrict, quarantine, retire-review, or evidence missing.

The weekly board uses `RED`, `AMBER`, `GREEN`, and `PAUSED`:

- `RED`: critical/high security failure, scorecard `HOLD`/`STOP`, invalid evidence, or unauthorized state.
- `AMBER`: missing/stale evidence, insufficient sample, `IMPROVE`, or onboarding incomplete.
- `GREEN`: fresh live eval and security pass plus scorecard meeting the assignment bar.
- `PAUSED`: suspended, retiring, or retired assignment with no dispatch.

Every packet records both `execution_status` (`ok | error | skipped`) and `outcome_status` (`VERIFIED | HOLD | BLOCKED | NOOP | FAILED`). Scheduler success never means the workforce outcome passed.

## Monthly portfolio review

Aggregate at least three valid weekly packets plus the current deployment/scorecard evidence. The monthly packet reports runtime mix, evidence coverage, lifecycle state, utilization, costs, confidence-adjusted value, goal targets/latest values, limitations, and a decision for each assignment.

Allowed decisions are `SECURITY_AND_REMEDIATION_REVIEW`, `HOLD_FOR_EVIDENCE`, `IMPROVEMENT_PLAN`, `SCALE_REVIEW_ELIGIBLE`, `CONTINUE`, and `MAINTAIN_NO_DISPATCH`. All are advisory. “Scale review eligible” never changes workforce state by itself.

## Automation wiring

Preferred order:

```text
private receipts -> deterministic weekly script -> review JSON + Markdown
                                                -> Queen decision card
                                                -> optional n8n notification
                                                -> optional OpenClaw read-only query
```

Hermes cron is the best first trigger because the evidence is private and local. Keep the canonical script in this repo and use a thin profile-local launcher. Do not create the cron until these files are merged to the canonical branch and the existing scheduler registry has been re-audited. After creation, read back the exact job, run one bounded test, and report configuration separately from execution evidence.

n8n becomes useful when GitHub, ticketing, CRM, observability, or other SaaS systems must contribute events. It should normalize allowlisted fields and call the same deterministic collector or Queen ingress. Credentials stay in the n8n secret store; n8n payloads cannot assert approval, security pass, health, or promotion.

No live Agent-Estate HR workflow is activated by this repository. Every proposed n8n execution must follow `AuthenticatedIntake -> NormalizeValidate -> IdempotentLedgerUpsert -> PolicyRiskGate -> HumanApprovalResume -> DeterministicAction -> ReceiptMetrics -> ErrorDLQIncident`. The exact intake, approval, receipt, and forbidden fields are in `configs/n8n-agent-estate-handoff.example.json`.

## Commands

```powershell
python scripts/validate_agent_workforce.py
python scripts/validate_agent_governance.py
python scripts/render_weekly_agent_review.py --evidence-root <private-evidence-dir> --output <private-review.md> --json-output <private-review.json>
python scripts/render_monthly_agent_portfolio_review.py --weekly-reviews-root <private-weekly-dir> --evidence-root <private-evidence-dir> --period-start <iso-start> --period-end <iso-end> --output <private-monthly.md> --json-output <private-monthly.json>
python scripts/test_agent_workforce.py
python scripts/test_agent_governance.py
python scripts/test_monthly_agent_portfolio_review.py
```

The checked-in roster is an example contract. Real receipts and weekly packets belong in the private SIS/Starlight runtime sink, not Git.
