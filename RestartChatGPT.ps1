# Reinicia la app de ChatGPT (Windows)
$chatGptExe = Join-Path $env:LOCALAPPDATA 'Programs\ChatGPT\ChatGPT.exe'

if (-not (Test-Path $chatGptExe)) {
    Write-Output "ChatGPT.exe no se encontro en $chatGptExe. Ajusta la ruta si lo instalaste en otro lugar."
    exit 1
}

$chatGptProcesses = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -like 'ChatGPT*' }

if ($chatGptProcesses) {
    $chatGptProcesses | Stop-Process -Force
    Start-Sleep -Milliseconds 800
}

Start-Process -FilePath $chatGptExe -WorkingDirectory (Split-Path $chatGptExe)

if ($chatGptProcesses) {
    Write-Output 'ChatGPT reiniciado.'
} else {
    Write-Output 'ChatGPT iniciado.'
}
