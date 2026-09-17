$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$required = @(
  "README.md",
  "configs/hermes-profiles.example.json",
  "configs/openclaw-gateway.example.json",
  "configs/deepagents-harness.example.yaml",
  "configs/mcp-trust-tiers.example.json",
  "configs/starlight-queen-control-plane.example.json",
  "configs/agent-access-bundle.example.json",
  "configs/agent-workforce.example.json",
  "configs/swarm-mission.example.json",
  "configs/n8n-agent-estate-handoff.example.json",
  "docs/swarm-roles.md",
  "docs/control-plane-workflow.md",
  "docs/sis-memory-provenance.md",
  "docs/health-checks.md",
  "docs/deployment-recipes.md",
  "docs/agent-portfolio/STARLIGHT_INTELLIGENCE_CANONICAL_PORTFOLIO.md",
  "docs/operations/AGENT_ECONOMICS_AND_CAPABILITY.md",
  "docs/operations/AI_AGENT_HR_OPERATING_SYSTEM.md",
  "docs/operations/STARLIGHT_QUEEN_AGENT_ESTATE_OS.md",
  "observability/README.md",
  "observability/metric-catalog.v1.json",
  "observability/adoption-registry.v1.json",
  "schemas/agent-deployment/agent-deployment.schema.json",
  "schemas/agent-run-receipt/agent-run-receipt.schema.json",
  "schemas/agent-scorecard/agent-scorecard.schema.json",
  "schemas/queen-control-plane/queen-control-plane.schema.json",
  "schemas/agent-access-bundle/agent-access-bundle.schema.json",
  "schemas/agent-workforce/agent-workforce.schema.json",
  "schemas/agent-workforce-review/agent-workforce-review.schema.json",
  "schemas/agent-portfolio-review/agent-portfolio-review.schema.json",
  "schemas/swarm-mission/swarm-mission.schema.json",
  "schemas/n8n-agent-automation-handoff/n8n-agent-automation-handoff.schema.json",
  "scripts/validate_agent_observability.py",
  "scripts/calculate_agent_scorecard.py",
  "scripts/test_agent_scorecard.py",
  "scripts/validate_agent_governance.py",
  "scripts/test_agent_governance.py",
  "scripts/validate_agent_workforce.py",
  "scripts/render_weekly_agent_review.py",
  "scripts/test_agent_workforce.py",
  "scripts/render_monthly_agent_portfolio_review.py",
  "scripts/test_monthly_agent_portfolio_review.py",
  "portfolio/canonical-portfolio.v1.json",
  "portfolio/canonical-portfolio.manifest.json",
  "schemas/agent-portfolio/canonical-portfolio.schema.json",
  "scripts/generate_canonical_portfolio.py",
  "scripts/validate_canonical_portfolio.py",
  "scripts/test_canonical_portfolio.py",
  "templates/codex-maintainer.md",
  "templates/AGENTS.md"
)

foreach ($file in $required) {
  $path = Join-Path $root $file
  if (-not (Test-Path $path)) {
    throw "Missing required file: $file"
  }
}

Get-Content -Raw (Join-Path $root "configs/hermes-profiles.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "configs/openclaw-gateway.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "configs/mcp-trust-tiers.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "configs/starlight-queen-control-plane.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "configs/agent-access-bundle.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "configs/agent-workforce.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "configs/swarm-mission.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "configs/n8n-agent-estate-handoff.example.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "observability/metric-catalog.v1.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "observability/adoption-registry.v1.json") | ConvertFrom-Json | Out-Null

foreach ($profile in Get-ChildItem (Join-Path $root "observability/deployments") -Filter "*.json") {
  Get-Content -Raw $profile.FullName | ConvertFrom-Json | Out-Null
}

Get-Content -Raw (Join-Path $root "portfolio/canonical-portfolio.v1.json") | ConvertFrom-Json | Out-Null
Get-Content -Raw (Join-Path $root "portfolio/canonical-portfolio.manifest.json") | ConvertFrom-Json | Out-Null

& python (Join-Path $root "scripts/generate_canonical_portfolio.py") --check
if ($LASTEXITCODE -ne 0) { throw "Canonical portfolio generation drift check failed." }
& python (Join-Path $root "scripts/validate_canonical_portfolio.py")
if ($LASTEXITCODE -ne 0) { throw "Canonical portfolio structural validation failed." }
& python (Join-Path $root "scripts/test_canonical_portfolio.py")
if ($LASTEXITCODE -ne 0) { throw "Canonical portfolio focused tests failed." }

& python (Join-Path $root "scripts/validate_agent_governance.py")
if ($LASTEXITCODE -ne 0) { throw "Agent governance validation failed." }
& python (Join-Path $root "scripts/test_agent_governance.py")
if ($LASTEXITCODE -ne 0) { throw "Agent governance focused tests failed." }
& python (Join-Path $root "scripts/validate_agent_workforce.py")
if ($LASTEXITCODE -ne 0) { throw "Agent workforce validation failed." }
& python (Join-Path $root "scripts/test_agent_workforce.py")
if ($LASTEXITCODE -ne 0) { throw "Agent workforce focused tests failed." }
& python (Join-Path $root "scripts/test_monthly_agent_portfolio_review.py")
if ($LASTEXITCODE -ne 0) { throw "Monthly agent portfolio review tests failed." }

$readme = Get-Content -Raw (Join-Path $root "README.md")
foreach ($needle in @("Codex", "Hermes", "OpenClaw", "DeepAgents", "SIS")) {
  if ($readme -notmatch [regex]::Escape($needle)) {
    throw "README missing required term: $needle"
  }
}

Write-Host "Architecture validation passed."
