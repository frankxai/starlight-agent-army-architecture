[CmdletBinding()]
param(
  [string]$RepoRoot
)

$ErrorActionPreference = 'Stop'

if (-not $RepoRoot) {
  $RepoRoot = Split-Path -Parent $PSScriptRoot
}

$portfolioPath = Join-Path $RepoRoot 'portfolio\canonical-portfolio.v1.json'
$civilizationPath = Join-Path $RepoRoot 'portfolio\civilization-portfolio.v2.json'
$graphPath = Join-Path $RepoRoot 'portfolio\civilization-graph.v2.json'
$templatePath = Join-Path $RepoRoot 'docs\visuals\agent-workflow-atlas.template.html'
$outputPath = Join-Path $RepoRoot 'docs\visuals\agent-workflow-atlas.html'

foreach ($path in @($portfolioPath, $civilizationPath, $graphPath, $templatePath)) {
  if (-not (Test-Path -LiteralPath $path)) {
    throw "Required atlas source is missing: $path"
  }
}

$portfolio = Get-Content -Raw -LiteralPath $portfolioPath | ConvertFrom-Json
$civilization = Get-Content -Raw -LiteralPath $civilizationPath | ConvertFrom-Json
$graph = Get-Content -Raw -LiteralPath $graphPath | ConvertFrom-Json

$swarms = foreach ($swarm in $portfolio.swarms) {
  [ordered]@{
    id = $swarm.id
    name = $swarm.name
    purpose = $swarm.purpose
    leadAgentId = $swarm.lead_agent_id
    visualWorld = $swarm.visual_world
    agents = @(
      foreach ($agent in $swarm.agents) {
        [ordered]@{
          id = $agent.id
          name = $agent.display_name
          role = $agent.role_title
          kind = $agent.role_kind
          profile = $agent.public_profile
          voice = $agent.voice
          skills = @($agent.skill_refs)
          capabilities = @($agent.capabilities)
          boundaries = @($agent.non_capabilities)
          signature = $agent.visual_dna.signature
          image = "../../assets/starlight-constellation/v1/agents/$($swarm.id)/$($agent.id).webp"
        }
      }
    )
  }
}

$rings = foreach ($ring in $civilization.rings) {
  [ordered]@{
    id = $ring.id
    number = $ring.number
    name = $ring.name
    vow = $ring.vow
    input = $ring.input
    output = $ring.output
    humanBoundary = $ring.human_boundary
    agents = @(
      foreach ($agent in $ring.agents) {
        [ordered]@{
          id = $agent.agent_id
          name = $agent.display_name
          role = $agent.role_title
          kind = $agent.role_kind
          cohort = $agent.portfolio_cohort
          status = $agent.profile_status
          purpose = $agent.purpose
          profile = $agent.public_profile
          voice = $agent.voice
          personality = @($agent.personality)
          workMode = $agent.work_mode
          skills = @($agent.skill_refs)
          capabilities = @($agent.capabilities)
          boundaries = @($agent.non_capabilities)
          stopConditions = @($agent.stop_conditions)
          escalationConditions = @($agent.escalation_conditions)
          morphology = $agent.visual.morphology_family
          assetStatus = $agent.visual.asset_status
          workflowIds = @($agent.graph.workflow_ids)
        }
      }
    )
  }
}

$workflows = foreach ($workflow in $graph.workflow_contracts) {
  [ordered]@{
    id = $workflow.id
    name = $workflow.name
    pattern = $workflow.pattern
    status = $workflow.status
    entryCriteria = $workflow.entry_criteria
    steps = @($workflow.steps)
    topology = $workflow.topology
    brakes = $workflow.brakes
    failurePath = $workflow.failure_path
    exitProof = $workflow.exit_proof
    writeback = $workflow.writeback
  }
}

$foundingCount = @($rings.agents | Where-Object cohort -eq 'founding-50').Count
$expansionCount = @($rings.agents | Where-Object cohort -eq 'expansion-94').Count

$sourceTimestamp = @($portfolioPath, $civilizationPath, $graphPath, $templatePath) |
  ForEach-Object { (Get-Item -LiteralPath $_).LastWriteTimeUtc } |
  Sort-Object -Descending |
  Select-Object -First 1

$payload = [ordered]@{
  compiledAtUtc = $sourceTimestamp.ToString('o')
  sources = [ordered]@{
    canonicalPortfolio = [ordered]@{
      path = 'portfolio/canonical-portfolio.v1.json'
      version = $portfolio.portfolio_version
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $portfolioPath).Hash.ToLowerInvariant()
    }
    civilizationPortfolio = [ordered]@{
      path = 'portfolio/civilization-portfolio.v2.json'
      version = $civilization.portfolio_version
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $civilizationPath).Hash.ToLowerInvariant()
    }
    civilizationGraph = [ordered]@{
      path = 'portfolio/civilization-graph.v2.json'
      sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $graphPath).Hash.ToLowerInvariant()
    }
  }
  counts = [ordered]@{
    constellations = @($swarms).Count
    foundingAgents = $foundingCount
    expansionAgents = $expansionCount
    agents = $foundingCount + $expansionCount
    rings = @($rings).Count
    workflows = @($workflows).Count
  }
  swarms = @($swarms)
  rings = @($rings)
  workflows = @($workflows)
  candidate = [ordered]@{
    id = 'lyra-v15-functional-identity-lock-v1'
    name = 'Lyra V1.5 functional identity lock'
    status = 'iterate'
    score = 25
    maxScore = 30
    image = '../../assets/starlight-constellation/v2-preview/next-pass/foundation-application-quartet/candidates/lyra-v15-functional-identity-lock-v1.png'
    referenceImage = '../../assets/starlight-constellation/v1/agents/intelligence-research/lyra-research-conductor.webp'
    prompt = '../../assets/starlight-constellation/v2-preview/next-pass/foundation-application-quartet/prompts/lyra-v15-functional-identity-lock-v1.json'
    review = '../../assets/starlight-constellation/v2-preview/next-pass/foundation-application-quartet/reviews/lyra-v15-functional-identity-lock-v1.quality-review.md'
    nextChange = 'Keep the exact face, palette, proportions, and stage; make only the integrated three-input-to-one-review-packet function unmistakable.'
  }
}

$json = $payload | ConvertTo-Json -Depth 30 -Compress
$json = $json.Replace('</', '<\/')
$template = Get-Content -Raw -LiteralPath $templatePath

if (-not $template.Contains('/*__STARLIGHT_ATLAS_DATA__*/')) {
  throw 'Atlas template is missing the data placeholder.'
}

$compiled = $template.Replace('/*__STARLIGHT_ATLAS_DATA__*/', $json)
[System.IO.File]::WriteAllText($outputPath, $compiled, [System.Text.UTF8Encoding]::new($false))

Write-Output "Built $outputPath"
Write-Output "Agents: $($payload.counts.agents) | Workflows: $($payload.counts.workflows) | Constellations: $($payload.counts.constellations)"
