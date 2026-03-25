param ()

<#
 .SYNOPSIS
    Muestra rápidamente la versión actual del workspace y su estado respecto a la nube.

 .DESCRIPTION
    Este script usa Git para imprimir el commit activo, la sucursal y si estamos adelante/atrás de origin.
    Está pensado para ejecutarse sin abrir macros ni paneles, basta abrir una terminal en la carpeta raíz.
 #>

try {
    $branch = git rev-parse --abbrev-ref HEAD 2>$null
    if (-not $branch) {
        throw "No se pudo determinar la rama activa."
    }
    Write-Host "Rama activa: $branch"

    $status = git status -sb
    Write-Host ""
    Write-Host "Estado del árbol:"
    Write-Host $status

    $commit = git log -1 --oneline 2>$null
    if ($commit) {
        Write-Host ""
        Write-Host "Último commit:"
        Write-Host $commit
    }
}
catch {
    Write-Host "No se pudo obtener la versión: $($_.Exception.Message)" -ForegroundColor Yellow
}
