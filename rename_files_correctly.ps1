# Script to rename files to reflect their actual creation timestamps
$latestDir = "agents/LATEST"

Get-ChildItem $latestDir -Filter "*.json" | ForEach-Object {
    $creationTime = $_.CreationTime
    $formattedTime = $creationTime.ToString("yyyy-MM-dd_HH-mm-ss")
    
    # Extract the category and description from the current filename
    $currentName = $_.Name
    if ($currentName -match "(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2})_(.+)_v(\d+\.\d+\.\d+)_(.+)\.json") {
        $category = $matches[2]
        $version = $matches[3]
        $status = $matches[4]
        
        $newName = "${formattedTime}_${category}_v${version}_${status}.json"
        
        Write-Host "Renaming: $currentName"
        Write-Host "To: $newName"
        Write-Host "Actual Creation Time: $creationTime"
        Write-Host "---"
        
        # Actually rename the files
        Rename-Item $_.FullName $newName
    }
} 