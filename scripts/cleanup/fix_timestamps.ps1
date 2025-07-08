# Fix January 2025 Timestamps Script
# This script updates all 2025-01 timestamps to 2025-07-07T16:00:00Z

Write-Host "Starting timestamp correction process..." -ForegroundColor Green

# Get all JSON files with 2025-01 timestamps
$files = Get-ChildItem -Recurse -Include "*.json" | Select-String "2025-01" | Select-Object -ExpandProperty Filename | Sort-Object | Get-Unique

Write-Host "Found $($files.Count) files with January 2025 timestamps" -ForegroundColor Yellow

$fixedCount = 0

foreach ($file in $files) {
    try {
        $content = Get-Content $file -Raw
        $originalContent = $content
        
        # Replace all 2025-01 timestamps with 2025-07-07T16:00:00Z
        $content = $content -replace '"2025-01-\d{2}T\d{2}:\d{2}:\d{2}Z"', '"2025-07-07T16:00:00Z"'
        $content = $content -replace '"2025-01-\d{2}"', '"2025-07-07"'
        
        # Only write if content changed
        if ($content -ne $originalContent) {
            Set-Content -Path $file -Value $content -NoNewline
            $fixedCount++
            Write-Host "Fixed: $file" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Error processing $file : $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "Timestamp correction completed. Fixed $fixedCount files." -ForegroundColor Green

# Verify the fix
$remainingFiles = Get-ChildItem -Recurse -Include "*.json" | Select-String "2025-01" | Select-Object -ExpandProperty Filename | Sort-Object | Get-Unique

if ($remainingFiles.Count -eq 0) {
    Write-Host "All January 2025 timestamps have been successfully corrected!" -ForegroundColor Green
} else {
    Write-Host "Warning: $($remainingFiles.Count) files still contain January 2025 timestamps:" -ForegroundColor Yellow
    foreach ($file in $remainingFiles) {
        Write-Host "  $file" -ForegroundColor Yellow
    }
} 