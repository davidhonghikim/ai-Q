#!/usr/bin/env pwsh

# AI-Q Timestamp Fix Script
# Purpose: Fix all January 2025 timestamp violations by updating to July 2025+
# Created: 2025-07-07T16:30:00Z

param(
    [string]$ProjectRoot = "E:\kos\ai-Q",
    [string]$BackupDir = "E:\kos\ai-Q\backups\timestamp-fix-$(Get-Date -Format 'yyyy-MM-dd-HHmmss')"
)

Write-Host "=== AI-Q Timestamp Fix Script ===" -ForegroundColor Green
Write-Host "Project Root: $ProjectRoot" -ForegroundColor Yellow
Write-Host "Backup Directory: $BackupDir" -ForegroundColor Yellow
Write-Host ""

# Create backup directory
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir -Force | Out-Null
    Write-Host "Created backup directory: $BackupDir" -ForegroundColor Green
}

# Find all JSON files with 2025-01 timestamps
Write-Host "Scanning for files with January 2025 timestamps..." -ForegroundColor Cyan
$filesWithJan2025 = Get-ChildItem -Path $ProjectRoot -Recurse -Include "*.json" | 
    Where-Object { (Get-Content $_.FullName -Raw) -match "2025-01" }

Write-Host "Found $($filesWithJan2025.Count) files with January 2025 timestamps" -ForegroundColor Yellow

if ($filesWithJan2025.Count -eq 0) {
    Write-Host "No files with January 2025 timestamps found. Exiting." -ForegroundColor Green
    exit 0
}

# Process each file
$processedCount = 0
$errorCount = 0
$currentTime = Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"

foreach ($file in $filesWithJan2025) {
    try {
        Write-Host "Processing: $($file.FullName)" -ForegroundColor White
        
        # Create backup
        $backupPath = Join-Path $BackupDir $file.Name
        Copy-Item $file.FullName $backupPath -Force
        
        # Read file content
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Replace various timestamp patterns
        $originalContent = $content
        
        # Pattern 1: "2025-01-XX" dates
        $content = $content -replace '"2025-01-(\d{2})"', '"2025-07-$1"'
        
        # Pattern 2: "2025-01-XXT" timestamps
        $content = $content -replace '"2025-01-(\d{2})T', '"2025-07-$1T'
        
        # Pattern 3: "2025-01-XXTXX:XX:XXZ" full timestamps
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z"', '"2025-07-$1T$2:$3:$4Z"'
        
        # Pattern 4: "2025-01-XXTXX:XX:XX" timestamps without Z
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})"', '"2025-07-$1T$2:$3:$4"'
        
        # Pattern 5: "2025-01-XXTXX:XX:XX.XXXZ" timestamps with milliseconds
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)Z"', '"2025-07-$1T$2:$3:$4.$5Z"'
        
        # Pattern 6: "2025-01-XXTXX:XX:XX.XXX" timestamps with milliseconds without Z
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)"', '"2025-07-$1T$2:$3:$4.$5"'
        
        # Pattern 7: "2025-01-XXTXX:XX:XX.XXX+XX:XX" timestamps with timezone
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)\+(\d{2}):(\d{2})"', '"2025-07-$1T$2:$3:$4.$5+$6:$7"'
        
        # Pattern 8: "2025-01-XXTXX:XX:XX+XX:XX" timestamps with timezone
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\+(\d{2}):(\d{2})"', '"2025-07-$1T$2:$3:$4+$5:$6"'
        
        # Pattern 9: "2025-01-XXTXX:XX:XX-XX:XX" timestamps with negative timezone
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})-(\d{2}):(\d{2})"', '"2025-07-$1T$2:$3:$4-$5:$6"'
        
        # Pattern 10: "2025-01-XXTXX:XX:XX.XXX-XX:XX" timestamps with milliseconds and negative timezone
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)-(\d{2}):(\d{2})"', '"2025-07-$1T$2:$3:$4.$5-$6:$7"'
        
        # Pattern 11: "2025-01-XXTXX:XX:XX.XXX+XX:XX" timestamps with milliseconds and positive timezone
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)\+(\d{2}):(\d{2})"', '"2025-07-$1T$2:$3:$4.$5+$6:$7"'
        
        # Pattern 12: "2025-01-XXTXX:XX:XX.XXX+XXXX" timestamps with milliseconds and timezone without colon
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)\+(\d{4})"', '"2025-07-$1T$2:$3:$4.$5+$6"'
        
        # Pattern 13: "2025-01-XXTXX:XX:XX.XXX-XXXX" timestamps with milliseconds and negative timezone without colon
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d+)-(\d{4})"', '"2025-07-$1T$2:$3:$4.$5-$6"'
        
        # Pattern 14: "2025-01-XXTXX:XX:XX+XXXX" timestamps with timezone without colon
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})\+(\d{4})"', '"2025-07-$1T$2:$3:$4+$5"'
        
        # Pattern 15: "2025-01-XXTXX:XX:XX-XXXX" timestamps with negative timezone without colon
        $content = $content -replace '"2025-01-(\d{2})T(\d{2}):(\d{2}):(\d{2})-(\d{4})"', '"2025-07-$1T$2:$3:$4-$5"'
        
        # Check if content was actually changed
        if ($content -eq $originalContent) {
            Write-Host "  No changes needed" -ForegroundColor Gray
            continue
        }
        
        # Write updated content back to file
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        
        $processedCount++
        Write-Host "  ✓ Updated timestamps" -ForegroundColor Green
        
    } catch {
        $errorCount++
        Write-Host "  ✗ Error processing file: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Timestamp Fix Summary ===" -ForegroundColor Green
Write-Host "Files processed: $processedCount" -ForegroundColor Cyan
Write-Host "Errors encountered: $errorCount" -ForegroundColor Red
Write-Host "Backup location: $BackupDir" -ForegroundColor Yellow

# Verify no January 2025 timestamps remain
Write-Host ""
Write-Host "Verifying no January 2025 timestamps remain..." -ForegroundColor Cyan
$remainingJan2025 = Get-ChildItem -Path $ProjectRoot -Recurse -Include "*.json" | 
    Where-Object { (Get-Content $_.FullName -Raw) -match "2025-01" }

if ($remainingJan2025.Count -eq 0) {
    Write-Host "✓ All January 2025 timestamps have been successfully updated!" -ForegroundColor Green
} else {
    Write-Host "✗ $($remainingJan2025.Count) files still contain January 2025 timestamps:" -ForegroundColor Red
    foreach ($file in $remainingJan2025) {
        Write-Host "  - $($file.FullName)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Timestamp fix operation completed at: $currentTime" -ForegroundColor Green 