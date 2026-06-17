$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$required = @(
  "README.md",
  "configs/hermes-profiles.example.json",
  "configs/openclaw-gateway.example.json",
  "configs/deepagents-harness.example.yaml",
  "configs/mcp-trust-tiers.example.json",
  "docs/swarm-roles.md",
  "docs/control-plane-workflow.md",
  "docs/sis-memory-provenance.md",
  "docs/health-checks.md",
  "docs/deployment-recipes.md",
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

$readme = Get-Content -Raw (Join-Path $root "README.md")
foreach ($needle in @("Codex", "Hermes", "OpenClaw", "DeepAgents", "SIS")) {
  if ($readme -notmatch [regex]::Escape($needle)) {
    throw "README missing required term: $needle"
  }
}

Write-Host "Architecture validation passed."
