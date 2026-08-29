# Business Ops Supervisor KB (private internal)

## Law
Supervisor architecture, not chatbot soup. Every worker needs identity, scope, review boundary, exit condition, and human owner.

## Stack layers
1. **Human cockpit** — Telegram / Desktop (Frank)
2. **Supervisor** — `biz-ops-supervisor` under Starlight Operator
3. **Specialists** — `biz-*` cards (capture, CoS, content, runway, …)
4. **Runtimes** — Hermes (private), coding CLIs (gstack/Agent HQ for code), optional Paperclip-class org UI later
5. **Evidence** — work ledger, receipts, draft PRs, CRM/ledger SSOT

## Never
- Auto-publish, auto-pay, auto-send contracts
- Private vault on public product agents
- Parallel second control plane without promoting into this SSOT
