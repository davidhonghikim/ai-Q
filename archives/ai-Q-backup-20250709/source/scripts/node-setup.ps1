# Node.js Setup Script for AI-Q Project
# This script sets up the portable Node.js installation for the project

param(
    [switch]$Test,
    [switch]$Install,
    [switch]$Clean
)

$NodePath = ".\nodejs-portable\node-v20.11.0-win-x64"
$NodeExe = "$NodePath\node.exe"
$NpmExe = "$NodePath\npm.cmd"

Write-Host "AI-Q Node.js Setup Script" -ForegroundColor Green
Write-Host "=========================" -ForegroundColor Green

if ($Test) {
    Write-Host "Testing Node.js installation..." -ForegroundColor Yellow
    
    if (Test-Path $NodeExe) {
        Write-Host "✓ Node.js found at: $NodeExe" -ForegroundColor Green
        $nodeVersion = & $NodeExe --version
        Write-Host "✓ Node.js version: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Node.js not found at: $NodeExe" -ForegroundColor Red
        exit 1
    }
    
    if (Test-Path $NpmExe) {
        Write-Host "✓ npm found at: $NpmExe" -ForegroundColor Green
        $npmVersion = & $NpmExe --version
        Write-Host "✓ npm version: $npmVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ npm not found at: $NpmExe" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✓ Node.js installation test passed!" -ForegroundColor Green
}

if ($Install) {
    Write-Host "Installing project dependencies..." -ForegroundColor Yellow
    
    # Set environment variables for this session
    $env:PATH = "$NodePath;$env:PATH"
    
    # Install dependencies using the working package.json
    Write-Host "Installing dependencies from package.json..." -ForegroundColor Yellow
    & $NpmExe install
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

if ($Clean) {
    Write-Host "Cleaning up package.json files..." -ForegroundColor Yellow
    
    # Remove all package.json variants except the main one
    $filesToRemove = @(
        "package-conservative.json",
        "package-batch1.json", 
        "package-batch2.json",
        "package-clean.json",
        "package-current.json",
        "package-minimal.json",
        "package.json.backup"
    )
    
    foreach ($file in $filesToRemove) {
        if (Test-Path $file) {
            Remove-Item $file
            Write-Host "✓ Removed: $file" -ForegroundColor Green
        }
    }
    
    # Remove nodejs-portable.zip and installer
    if (Test-Path "nodejs-portable.zip") {
        Remove-Item "nodejs-portable.zip"
        Write-Host "✓ Removed: nodejs-portable.zip" -ForegroundColor Green
    }
    
    if (Test-Path "nodejs-installer.msi") {
        Remove-Item "nodejs-installer.msi"
        Write-Host "✓ Removed: nodejs-installer.msi" -ForegroundColor Green
    }
    
    Write-Host "✓ Cleanup completed!" -ForegroundColor Green
}

if (-not $Test -and -not $Install -and -not $Clean) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\scripts\node-setup.ps1 -Test    # Test Node.js installation" -ForegroundColor White
    Write-Host "  .\scripts\node-setup.ps1 -Install # Install dependencies" -ForegroundColor White
    Write-Host "  .\scripts\node-setup.ps1 -Clean   # Clean up package.json files" -ForegroundColor White
    Write-Host "  .\scripts\node-setup.ps1 -Test -Install -Clean # Run all" -ForegroundColor White
} 