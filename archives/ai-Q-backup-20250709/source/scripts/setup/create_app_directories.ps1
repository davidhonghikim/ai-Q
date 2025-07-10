# Create app directories for pantry ingredients
$apps = @("comfyui", "n8n", "penpot", "openwebui")
$types = @("tools", "skills", "tasks", "modules")

foreach ($app in $apps) {
    $appPath = "kitchen\pantry\ingredients\$app"
    if (!(Test-Path $appPath)) {
        New-Item -ItemType Directory -Path $appPath -Force
        Write-Host "Created $appPath"
    }
    
    foreach ($type in $types) {
        $typePath = "$appPath\$type"
        if (!(Test-Path $typePath)) {
            New-Item -ItemType Directory -Path $typePath -Force
            Write-Host "Created $typePath"
        }
    }
}

Write-Host "All app directories created successfully!" 