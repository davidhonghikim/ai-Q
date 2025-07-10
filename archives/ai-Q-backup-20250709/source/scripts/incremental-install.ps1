# Incremental Dependency Installation Script for AI-Q Project
# This script installs dependencies in stages to avoid conflicts

param(
    [switch]$Stage1,
    [switch]$Stage2,
    [switch]$Stage3,
    [switch]$Stage4,
    [switch]$All,
    [switch]$Clean
)

$NodePath = ".\nodejs-portable\node-v20.11.0-win-x64"
$NodeExe = "$NodePath\node.exe"
$NpmExe = "$NodePath\npm.cmd"

Write-Host "AI-Q Incremental Installation Script" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green

function Test-NodeJS {
    if (Test-Path $NodeExe) {
        Write-Host "✓ Node.js found at: $NodeExe" -ForegroundColor Green
        $nodeVersion = & $NodeExe --version
        Write-Host "✓ Node.js version: $nodeVersion" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Node.js not found at: $NodeExe" -ForegroundColor Red
        return $false
    }
}

function Install-Stage1 {
    Write-Host "Stage 1: Installing minimal core dependencies..." -ForegroundColor Yellow
    
    # Copy minimal package.json
    Copy-Item "package-minimal.json" "package.json" -Force
    Write-Host "✓ Using package-minimal.json" -ForegroundColor Green
    
    # Install dependencies
    Write-Host "Installing minimal dependencies..." -ForegroundColor Yellow
    & $NpmExe install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Stage 1 completed successfully!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Stage 1 failed" -ForegroundColor Red
        return $false
    }
}

function Install-Stage2 {
    Write-Host "Stage 2: Installing basic development dependencies..." -ForegroundColor Yellow
    
    # Copy batch1 package.json
    Copy-Item "package-batch1.json" "package.json" -Force
    Write-Host "✓ Using package-batch1.json" -ForegroundColor Green
    
    # Install dependencies
    Write-Host "Installing basic development dependencies..." -ForegroundColor Yellow
    & $NpmExe install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Stage 2 completed successfully!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Stage 2 failed" -ForegroundColor Red
        return $false
    }
}

function Install-Stage3 {
    Write-Host "Stage 3: Installing enhanced development dependencies..." -ForegroundColor Yellow
    
    # Copy batch2 package.json
    Copy-Item "package-batch2.json" "package.json" -Force
    Write-Host "✓ Using package-batch2.json" -ForegroundColor Green
    
    # Install dependencies
    Write-Host "Installing enhanced development dependencies..." -ForegroundColor Yellow
    & $NpmExe install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Stage 3 completed successfully!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Stage 3 failed" -ForegroundColor Red
        return $false
    }
}

function Install-Stage4 {
    Write-Host "Stage 4: Installing full feature dependencies..." -ForegroundColor Yellow
    
    # Copy current package.json (full features)
    Copy-Item "package-current.json" "package.json" -Force
    Write-Host "✓ Using package-current.json" -ForegroundColor Green
    
    # Install dependencies
    Write-Host "Installing full feature dependencies..." -ForegroundColor Yellow
    & $NpmExe install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Stage 4 completed successfully!" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✗ Stage 4 failed" -ForegroundColor Red
        return $false
    }
}

function Clean-Installation {
    Write-Host "Cleaning installation..." -ForegroundColor Yellow
    
    # Remove node_modules and package-lock.json
    if (Test-Path "node_modules") {
        Remove-Item "node_modules" -Recurse -Force
        Write-Host "✓ Removed node_modules" -ForegroundColor Green
    }
    
    if (Test-Path "package-lock.json") {
        Remove-Item "package-lock.json" -Force
        Write-Host "✓ Removed package-lock.json" -ForegroundColor Green
    }
    
    # Restore original package.json
    Copy-Item "package-minimal.json" "package.json" -Force
    Write-Host "✓ Restored minimal package.json" -ForegroundColor Green
    
    Write-Host "✓ Cleanup completed!" -ForegroundColor Green
}

# Main execution
if (-not (Test-NodeJS)) {
    exit 1
}

if ($Clean) {
    Clean-Installation
    exit 0
}

if ($All) {
    Write-Host "Running all installation stages..." -ForegroundColor Yellow
    
    if (-not (Install-Stage1)) { exit 1 }
    if (-not (Install-Stage2)) { exit 1 }
    if (-not (Install-Stage3)) { exit 1 }
    if (-not (Install-Stage4)) { exit 1 }
    
    Write-Host "✓ All stages completed successfully!" -ForegroundColor Green
    exit 0
}

if ($Stage1) {
    Install-Stage1
    exit $LASTEXITCODE
}

if ($Stage2) {
    Install-Stage2
    exit $LASTEXITCODE
}

if ($Stage3) {
    Install-Stage3
    exit $LASTEXITCODE
}

if ($Stage4) {
    Install-Stage4
    exit $LASTEXITCODE
}

# Show usage if no parameters provided
Write-Host "Usage:" -ForegroundColor Yellow
Write-Host "  .\scripts\incremental-install.ps1 -Stage1    # Install minimal dependencies" -ForegroundColor White
Write-Host "  .\scripts\incremental-install.ps1 -Stage2    # Install basic dev dependencies" -ForegroundColor White
Write-Host "  .\scripts\incremental-install.ps1 -Stage3    # Install enhanced dev dependencies" -ForegroundColor White
Write-Host "  .\scripts\incremental-install.ps1 -Stage4    # Install full feature dependencies" -ForegroundColor White
Write-Host "  .\scripts\incremental-install.ps1 -All       # Run all stages in sequence" -ForegroundColor White
Write-Host "  .\scripts\incremental-install.ps1 -Clean     # Clean installation and start fresh" -ForegroundColor White 