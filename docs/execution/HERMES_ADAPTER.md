# Hermes profile adapter notes

## Starlight Operator
Map `cards/hosts/starlight-operator.json` → Hermes default/profile:
- SOUL.md ← soul_md content principles (merge carefully with existing Hermes SOUL)
- skills ← mind.skills
- tools ← will.tools_allow (Hermes-native names)
- memory ← private_vault via existing Hermes memory system

## Gen-Ω on Hermes (optional power users)
- Do not enable private vault tools
- Use user-scoped project memory only
- Prefer web body for customers

## Import checklist
1. validate_agent_cards.py green
2. Diff soul against live Hermes SOUL — never blind overwrite Frank's operator SOUL
3. Skill names must exist or be stubs
4. Telegram is human cockpit; bus remains SSOT for multi-agent tasks
