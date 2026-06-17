# Deployment Recipes

Starlight fleets are hybrid by default: private execution local, public surfaces in the cloud.

## Vercel

Best for:

- Dashboards
- Docs
- API routes
- Workflows
- Preview deployments

Use for `starlight-swarm`, public docs, lightweight agent status APIs, and operator cockpit surfaces that do not need local filesystem access.

## Railway

Best for:

- Always-on services
- Containers
- Gateways
- Worker APIs

Use for an OpenClaw gateway or model proxy only after auth, owner allowlists, secrets, and logs are configured.

## Cloudflare

Best for:

- Static docs
- Edge APIs
- Workers
- Durable Objects
- Public routing and protection

Use for public guide sites, edge routing, and low-latency API shells around agent systems.

## Local Machine

Best for:

- Private repos
- Filesystem access
- Personal MCP servers
- Hermes profiles
- Codex/Claude Code repo work

Keep local-only tools behind loopback, Tailscale, or another explicit private network boundary.
