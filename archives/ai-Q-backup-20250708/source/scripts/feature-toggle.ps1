# AI-Q Feature Toggle Script for Windows
# Allows easy enabling/disabling of system components

param(
    [Parameter(Mandatory=$false)]
    [string]$Action = "status",
    
    [Parameter(Mandatory=$false)]
    [string]$Feature = "",
    
    [Parameter(Mandatory=$false)]
    [string]$Category = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$Enable,
    
    [Parameter(Mandatory=$false)]
    [switch]$Disable,
    
    [Parameter(Mandatory=$false)]
    [switch]$List
)

$ConfigPath = "config/feature-flags.yml"
$ScriptPath = "scripts/feature-flag-parser.py"

function Get-YamlConfig {
    param([string]$Path)
    
    if (Test-Path $Path) {
        $content = Get-Content $Path -Raw
        # Simple YAML parsing for basic key-value pairs
        $yamlConfig = @{}
        $lines = $content -split "`n"
        
        foreach ($line in $lines) {
            if ($line -match "^\s*([^:]+):\s*(.+)$") {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                $yamlConfig[$key] = $value
            }
        }
        return $yamlConfig
    }
    return @{}
}

function Show-Status {
    Write-Host "=== AI-Q Feature Flags Status ===" -ForegroundColor Cyan
    
    if (Test-Path $ConfigPath) {
        # $config = Get-YamlConfig $ConfigPath  # Unused, so removed
        Write-Host "Configuration file: $ConfigPath" -ForegroundColor Green
        
        # Run Python script to get detailed status
        if (Test-Path $ScriptPath) {
            Write-Host "`nEnabled Components:" -ForegroundColor Yellow
            python $ScriptPath list-services
            
            Write-Host "`nFeature Details:" -ForegroundColor Yellow
            python $ScriptPath check
        }
    } else {
        Write-Host "Configuration file not found: $ConfigPath" -ForegroundColor Red
    }
}

function Show-List {
    Write-Host "=== Available Features ===" -ForegroundColor Cyan
    
    $features = @(
        @{Category="Core"; Features=@("api_server", "web_dashboard", "health_monitoring")},
        @{Category="Databases"; Features=@("postgresql", "redis", "elasticsearch", "neo4j", "weaviate")},
        @{Category="Storage"; Features=@("minio")},
        @{Category="Monitoring"; Features=@("prometheus", "grafana", "cadvisor")},
        @{Category="AI/ML"; Features=@("rag", "vector_search", "graph_analytics", "content_analysis")},
        @{Category="Development"; Features=@("hot_reload", "debug_mode", "verbose_logging")},
        @{Category="Security"; Features=@("authentication", "ssl_enabled", "cors_enabled")},
        @{Category="Performance"; Features=@("caching_enabled", "compression_enabled", "rate_limiting")},
        @{Category="Integrations"; Features=@("openai_enabled", "huggingface_enabled", "external_apis")}
    )
    
    foreach ($category in $features) {
        Write-Host "`n$($category.Category):" -ForegroundColor Yellow
        foreach ($feature in $category.Features) {
            Write-Host "  - $feature" -ForegroundColor White
        }
    }
}

function Set-FeatureFlag {
    param(
        [string]$Category,
        [string]$Feature,
        [bool]$Enable
    )
    
    if (-not (Test-Path $ConfigPath)) {
        Write-Host "Configuration file not found: $ConfigPath" -ForegroundColor Red
        return
    }
    
    $content = Get-Content $ConfigPath -Raw
    $lines = $content -split "`n"
    $newLines = @()
    $inCategory = $false
    $found = $false
    
    foreach ($line in $lines) {
        if ($line -match "^\s*$Category\s*:") {
            $inCategory = $true
            $newLines += $line
        } elseif ($inCategory -and $line -match "^\s*$Feature\s*:") {
            $newLines += "  $Feature`: $($Enable.ToString().ToLower())"
            $found = $true
        } elseif ($inCategory -and $line -match "^\s*[a-zA-Z]") {
            $inCategory = $false
            $newLines += $line
        } else {
            $newLines += $line
        }
    }
    
    if (-not $found) {
        Write-Host "Feature '$Feature' not found in category '$Category'" -ForegroundColor Red
        return
    }
    
    $newLines | Set-Content $ConfigPath
    Write-Host "Feature '$Category.$Feature' set to: $($Enable.ToString().ToLower())" -ForegroundColor Green
    
    # Regenerate configurations
    if (Test-Path $ScriptPath) {
        Write-Host "Regenerating configurations..." -ForegroundColor Yellow
        python $ScriptPath generate-compose
        python $ScriptPath generate-env
    }
}

function Start-DynamicSystem {
    Write-Host "Starting AI-Q Dynamic System..." -ForegroundColor Cyan
    
    if (Test-Path "scripts/start-dynamic.sh") {
        # Convert to Windows command
        Write-Host "Running dynamic startup..." -ForegroundColor Yellow
        bash scripts/start-dynamic.sh
    } else {
        Write-Host "Dynamic startup script not found" -ForegroundColor Red
    }
}

# Main script logic
switch ($Action.ToLower()) {
    "status" {
        Show-Status
    }
    "list" {
        Show-List
    }
    "toggle" {
        if ($Category -and $Feature) {
            if ($Enable) {
                Set-FeatureFlag -Category $Category -Feature $Feature -Enable $true
            } elseif ($Disable) {
                Set-FeatureFlag -Category $Category -Feature $Feature -Enable $false
            } else {
                Write-Host "Use -Enable or -Disable flag" -ForegroundColor Red
            }
        } else {
            Write-Host "Please specify -Category and -Feature" -ForegroundColor Red
        }
    }
    "start" {
        Start-DynamicSystem
    }
    "generate" {
        if (Test-Path $ScriptPath) {
            Write-Host "Generating configurations..." -ForegroundColor Yellow
            python $ScriptPath generate-compose
            python $ScriptPath generate-env
        } else {
            Write-Host "Feature flag parser not found: $ScriptPath" -ForegroundColor Red
        }
    }
    default {
        Write-Host "AI-Q Feature Toggle Script" -ForegroundColor Cyan
        Write-Host "Usage:" -ForegroundColor White
        Write-Host "  .\scripts\feature-toggle.ps1 status" -ForegroundColor Gray
        Write-Host "  .\scripts\feature-toggle.ps1 list" -ForegroundColor Gray
        Write-Host "  .\scripts\feature-toggle.ps1 toggle -Category databases -Feature redis -Enable" -ForegroundColor Gray
        Write-Host "  .\scripts\feature-toggle.ps1 toggle -Category databases -Feature redis -Disable" -ForegroundColor Gray
        Write-Host "  .\scripts\feature-toggle.ps1 generate" -ForegroundColor Gray
        Write-Host "  .\scripts\feature-toggle.ps1 start" -ForegroundColor Gray
    }
} 