$ErrorActionPreference = "Stop"

$DocPath = "C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\GF-EIM-IT-0000-2026-ESP_TEC-TURRIALBA-v10_revision_editorial.docx"
$LogPath = "C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\auditoria_editorial_work\revision_editorial_log.txt"
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null
$script:Log = New-Object System.Collections.Generic.List[string]

function Add-Log([string]$Text) { $script:Log.Add($Text) | Out-Null }
function Clean-Text($Paragraph) { return (($Paragraph.Range.Text -replace "[`r`a]", "") -replace "\s+", " ").Trim() }
function Set-ParaText($Paragraph, [string]$Text) { $Paragraph.Range.Text = $Text + "`r" }

function Replace-All([string]$FindText, [string]$ReplaceText) {
    $find = $script:Doc.Content.Find
    $find.ClearFormatting() | Out-Null
    $find.Replacement.ClearFormatting() | Out-Null
    [void]$find.Execute($FindText, $false, $false, $false, $false, $false, $true, 1, $false, $ReplaceText, 2)
    Add-Log "Reemplazo: $FindText -> $ReplaceText"
}

function Add-YellowNoteAfterParagraph($Paragraph, [string]$NoteText) {
    $rng = $Paragraph.Range.Duplicate
    $rng.Collapse(0) | Out-Null
    $start = $rng.Start
    $rng.InsertAfter($NoteText + "`r") | Out-Null
    $noteRange = $script:Doc.Range($start, $start + $NoteText.Length)
    $noteRange.HighlightColorIndex = 7
    $noteRange.Font.Bold = $true
    Add-Log "Nota amarilla insertada: $NoteText"
}

function Add-YellowNoteAfterTable([int]$TableIndex, [string]$NoteText) {
    $table = $script:Doc.Tables.Item($TableIndex)
    $rng = $table.Range.Duplicate
    $rng.Collapse(0) | Out-Null
    $start = $rng.Start
    $rng.InsertAfter("`r" + $NoteText + "`r") | Out-Null
    $noteRange = $script:Doc.Range($start + 1, $start + 1 + $NoteText.Length)
    $noteRange.HighlightColorIndex = 7
    $noteRange.Font.Bold = $true
    Add-Log "Nota amarilla insertada tras tabla ${TableIndex}: $NoteText"
}

$word = $null
$script:Doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $script:Doc = $word.Documents.Open($DocPath, $false, $false, $false, '', '', $false, '', '', 0, 0, $false, $false, 0, $true)
    $script:Doc.Repaginate()

    $replacements = @(
        @("CAPITULO", "CAPÍTULO"),
        @("1. OBJETO DE LA CONTRATACION", "1. OBJETO DE LA CONTRATACIÓN"),
        @("5. CONDICIONES GENERALES DE EJECUCION", "5. CONDICIONES GENERALES DE EJECUCIÓN"),
        @("ESPECIFICACIONES ARQUITECTONICAS Y CIVILES", "ESPECIFICACIONES ARQUITECTÓNICAS Y CIVILES"),
        @("ESPECIFICACIONES ELECTROMECANICAS", "ESPECIFICACIONES ELECTROMECÁNICAS"),
        @("1.2. DEMOLICIONES Y REMOCION DE ELEMENTOS", "1.2. DEMOLICIONES Y REMOCIÓN DE ELEMENTOS"),
        @("1.4. AISLAMIENTO TERMICO", "1.4. AISLAMIENTO TÉRMICO"),
        @("1.6. TRATAMIENTO ANTICORROSIVO EN ESTRUCTURA METALICA DE ENTRETECHO", "1.6. TRATAMIENTO ANTICORROSIVO EN ESTRUCTURA METÁLICA DE ENTRETECHO"),
        @("1.7. TAPICHEL DE VENTILACION DEL ENTRETECHO", "1.7. TAPICHEL DE VENTILACIÓN DEL ENTRETECHO"),
        @("1.10. ADECUACION DE SERVICIOS SANITARIOS", "1.10. ADECUACIÓN DE SERVICIOS SANITARIOS"),
        @("1.12. ALERO EXTERIOR: DEMOLICION Y CONSTRUCCION", "1.12. ALERO EXTERIOR: DEMOLICIÓN Y CONSTRUCCIÓN"),
        @("1.14. CONSTRUCCION DE SALA DE LACTANCIA", "1.14. CONSTRUCCIÓN DE SALA DE LACTANCIA"),
        @("1.15. CONSTRUCCION DE BODEGA DE SUMINISTROS", "1.15. CONSTRUCCIÓN DE BODEGA DE SUMINISTROS"),
        @("1.16. CONSTRUCCION DE ARCHIVO MUERTO", "1.16. CONSTRUCCIÓN DE ARCHIVO MUERTO"),
        @("1.17. REMODELACION DE PLATAFORMA", "1.17. REMODELACIÓN DE PLATAFORMA"),
        @("3.1. REPOSICION DE INFRAESTRUCTURA", "3.1. REPOSICIÓN DE INFRAESTRUCTURA"),
        @("3.6. DOCUMENTACION Y OTRAS CONSIDERACIONES", "3.6. DOCUMENTACIÓN Y OTRAS CONSIDERACIONES"),
        @("3.8. ESPECIFICACIONES TECNICAS DE CABLEADO ESTRUCTURADO", "3.8. ESPECIFICACIONES TÉCNICAS DE CABLEADO ESTRUCTURADO"),
        @("3.9. ESTANDAR DE ETIQUETADO", "3.9. ESTÁNDAR DE ETIQUETADO"),
        @("4.1. ILUMINACION DE EMERGENCIA", "4.1. ILUMINACIÓN DE EMERGENCIA"),
        @("4.2. SENALIZACION DE SEGURIDAD, EVACUACION Y ACCESIBILIDAD", "4.2. SEÑALIZACIÓN DE SEGURIDAD, EVACUACIÓN Y ACCESIBILIDAD"),
        @("4.3. EXTINTORES PORTATILES", "4.3. EXTINTORES PORTÁTILES"),
        @("5.1. PRUEBAS Y VERIFICACIONES PREVIAS A LA RECEPCION PROVISIONAL", "5.1. PRUEBAS Y VERIFICACIONES PREVIAS A LA RECEPCIÓN PROVISIONAL"),
        @("5.2. DOCUMENTOS PARA LA RECEPCION PROVISIONAL", "5.2. DOCUMENTOS PARA LA RECEPCIÓN PROVISIONAL"),
        @("5.3. RECEPCION PROVISIONAL", "5.3. RECEPCIÓN PROVISIONAL"),
        @("5.4. RECEPCION DEFINITIVA", "5.4. RECEPCIÓN DEFINITIVA"),
        @("5.6. PERIODO Y CONDICIONES DE GARANTIA", "5.6. PERÍODO Y CONDICIONES DE GARANTÍA"),
        @("5.7. CAPACITACION AL PERSONAL", "5.7. CAPACITACIÓN AL PERSONAL"),
        @("7. SISTEMA DE EVALUACION DE OFERTAS", "7. SISTEMA DE EVALUACIÓN DE OFERTAS"),
        @("INSTALACIONES ELECTRICAS", "INSTALACIONES ELÉCTRICAS"),
        @("El Contratista presentara", "El Contratista presentará"),
        @("El Contratista planificara", "El Contratista planificará"),
        @(" y ejecutara ", " y ejecutará "),
        @("Sera responsable", "Será responsable"),
        @("se repararan así", "se repararán así"),
        @("llevaran sellador", "llevarán sellador"),
        @("Area aproximada", "Área aproximada"),
        @("Areas intervenidas", "Áreas intervenidas"),
        @("25 años o mas", "25 años o más"),
        @("m2", "m²"),
        @("120V/15A", "120 V/15 A"),
        @("120V/60Hz", "120 V/60 Hz"),
        @("400m", "400 m"),
        @("10Gbps", "10 Gbps"),
        @("483mm.", "483 mm."),
        @("50x50x2mm", "50 x 50 x 2 mm"),
        @("61x61x19mm", "61 x 61 x 19 mm"),
        @("30x100mm", "30 x 100 mm"),
        @("30x200mm", "30 x 200 mm"),
        @("30x300mm", "30 x 300 mm"),
        @("54x200mm", "54 x 200 mm"),
        @("105x100mm", "105 x 100 mm"),
        @("54x300mm", "54 x 300 mm"),
        @("105x150mm", "105 x 150 mm"),
        @("105x200mm", "105 x 200 mm"),
        @("54x450mm", "54 x 450 mm"),
        @("105x300mm", "105 x 300 mm"),
        @("150x200mm", "150 x 200 mm"),
        @("105x450mm", "105 x 450 mm"),
        @("150x300mm", "150 x 300 mm"),
        @("5mm", "5 mm"),
        @("7mm", "7 mm"),
        @("12mm", "12 mm"),
        @("19mm", "19 mm"),
        @("4,9mm", "4,9 mm"),
        @("1,80m", "1,80 m"),
        @("Patch Cord de fibra Optica Duplex", "Patch Cord de fibra Óptica Duplex")
    )
    foreach ($pair in $replacements) { Replace-All $pair[0] $pair[1] }

    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Clean-Text $p
        if ($text -eq "1.16.6. Criterios de Aceptación y Medición") {
            Set-ParaText $p "1.16.5. Criterios de Aceptación y Medición"
        } elseif ($text -eq "1.27.4. Normativa Aplicable") {
            Set-ParaText $p "1.27.3. Normativa Aplicable"
        } elseif ($text -eq "1.27.5. Criterios de Aceptación y Forma de Medición y Pago") {
            Set-ParaText $p "1.27.4. Criterios de Aceptación y Forma de Medición y Pago"
        } elseif ($text -eq "2.4. INTRODUCCIÓN A LOS REQUERIMIENTOS TÉCNICOS ELECTROMECÁNICOS") {
            Set-ParaText $p "INTRODUCCIÓN A LOS REQUERIMIENTOS TÉCNICOS ELECTROMECÁNICOS"
        } elseif ($text -eq "2.2.4. Procedimiento Constructivo") {
            Set-ParaText $p "2.2.3. Procedimiento Constructivo"
        } elseif ($text -eq "2.2.5. Criterios de Aceptación y Medición") {
            Set-ParaText $p "2.2.4. Criterios de Aceptación y Medición"
        } elseif ($text -eq "2.5. DESCRIPCIÓN GENERAL DEL SISTEMA ELÉCTRICO") {
            Set-ParaText $p "2.3. DESCRIPCIÓN GENERAL DEL SISTEMA ELÉCTRICO"
        } elseif ($text -eq "2.X. SISTEMA DE PUESTA A TIERRA") {
            Set-ParaText $p "2.4. SISTEMA DE PUESTA A TIERRA"
        } elseif ($text -eq "2.X. TRANSFORMADOR DE DISTRIBUCIÓN Y ACOMETIDA") {
            Set-ParaText $p "2.5. TRANSFORMADOR DE DISTRIBUCIÓN Y ACOMETIDA"
        } elseif ($text -eq "3. CORTINA DE AIRE EN ACCESO PRINCIPAL") {
            Set-ParaText $p "2.16. CORTINA DE AIRE EN ACCESO PRINCIPAL"
        } elseif ($text -eq "2.15. SISTEMA DE ALARMA CONTRA ROBO Y SENSORES DE MOVIMIENTO") {
            Set-ParaText $p "2.17. SISTEMA DE ALARMA CONTRA ROBO Y SENSORES DE MOVIMIENTO"
        } elseif ($text -eq "2.16. SISTEMA DE DETECCIÓN DE INCENDIOS") {
            Set-ParaText $p "2.18. SISTEMA DE DETECCIÓN DE INCENDIOS"
        } elseif ($text -eq "2.17. SISTEMA DE VIDEOVIGILANCIA") {
            Set-ParaText $p "2.19. SISTEMA DE VIDEOVIGILANCIA"
        } elseif ($text -eq "2.17.1. Cámaras IP — Características Mínimas") {
            Set-ParaText $p "2.19.1. Cámaras IP — Características Mínimas"
        } elseif ($text -eq "2.17.2. Grabador NVR — Características Mínimas") {
            Set-ParaText $p "2.19.2. Grabador NVR — Características Mínimas"
        } elseif ($text -eq "2.17.3. Televisor de Monitoreo para Jefatura") {
            Set-ParaText $p "2.19.3. Televisor de Monitoreo para Jefatura"
        } elseif ($text -eq "2.18. CONTROL DE ACCESO PARA PUERTAS DE APERTURA MANUAL MEDIANTE TARJETA RFID") {
            Set-ParaText $p "2.20. CONTROL DE ACCESO PARA PUERTAS DE APERTURA MANUAL MEDIANTE TARJETA RFID"
        } elseif ($text -eq "2.18. BOTÓN Y ALARMA DE PÁNICO") {
            Set-ParaText $p "2.21. BOTÓN Y ALARMA DE PÁNICO"
        } elseif ($text -eq "2.15 RENOVACIÓN DEL SISTEMA HIDRONEUMÁTICO") {
            Set-ParaText $p "2.15. RENOVACIÓN DEL SISTEMA HIDRONEUMÁTICO"
        } elseif ($text -match "^2\.5\.(\d+)\.\s+(.*)$") {
            Set-ParaText $p ("2.3." + $Matches[1] + ". " + $Matches[2])
        }
    }

    $inside119 = $false
    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Clean-Text $p
        if ($text -like "1.19. CERRAMIENTO SUPERIOR DEL GARAJE*") { $inside119 = $true; continue }
        if ($text -like "1.20. REPARACIÓN INTEGRAL*") { $inside119 = $false }
        if ($inside119 -and $text -eq "1.20.1. Alcance") {
            Set-ParaText $p "1.19.1. Alcance"
            try { $p.Range.Style = $script:Doc.Styles.Item("Título 3") } catch {}
            $inside119 = $false
        }
    }

    foreach ($p in @($script:Doc.Paragraphs)) {
        $listString = ""
        try { $listString = $p.Range.ListFormat.ListString } catch {}
        if ($listString -match "^3\.6\.[1-7]\.$" -or $listString -match "^3\.7\.(2|3|4|5|6|7|8|9|10)\.$") {
            try { $p.Range.ListFormat.ApplyBulletDefault() | Out-Null } catch {}
        }
    }

    foreach ($p in @($script:Doc.Paragraphs)) {
        $styleName = ""
        $listString = ""
        try { $styleName = $p.Range.Style.NameLocal } catch {}
        try { $listString = $p.Range.ListFormat.ListString } catch {}
        if ($styleName -like "Título 3*" -and $listString -match "^\d+\.\d+\.\d+\.$") {
            $body = Clean-Text $p
            try { $p.Range.ListFormat.RemoveNumbers() | Out-Null } catch {}
            Set-ParaText $p ($listString + " " + $body)
            try { $p.Range.Style = $script:Doc.Styles.Item("Título 3") } catch {}
        }
    }

    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Clean-Text $p
        if ($text.Length -eq 0) { continue }
        $styleName = ""
        $listString = ""
        try { $styleName = $p.Range.Style.NameLocal } catch {}
        try { $listString = $p.Range.ListFormat.ListString } catch {}
        if (($styleName -like "Título 3*" -or $styleName -like "Título 4*") -and
            $text -notmatch "^\d+(\.\d+)*\.?\s+" -and
            $listString -notmatch "^\d+\.\d+\.\d+\.$" -and
            $text.Length -gt 70) {
            try { $p.Range.Style = $script:Doc.Styles.Item("Normal") } catch {}
        }
    }

    $heading2 = @(
        "2.3. DESCRIPCIÓN GENERAL DEL SISTEMA ELÉCTRICO",
        "2.4. SISTEMA DE PUESTA A TIERRA",
        "2.5. TRANSFORMADOR DE DISTRIBUCIÓN Y ACOMETIDA",
        "2.15. RENOVACIÓN DEL SISTEMA HIDRONEUMÁTICO",
        "2.16. CORTINA DE AIRE EN ACCESO PRINCIPAL",
        "2.17. SISTEMA DE ALARMA CONTRA ROBO Y SENSORES DE MOVIMIENTO",
        "2.18. SISTEMA DE DETECCIÓN DE INCENDIOS",
        "2.19. SISTEMA DE VIDEOVIGILANCIA",
        "2.20. CONTROL DE ACCESO PARA PUERTAS DE APERTURA MANUAL MEDIANTE TARJETA RFID",
        "2.21. BOTÓN Y ALARMA DE PÁNICO"
    )
    $heading3 = @(
        "2.2.3. Procedimiento Constructivo",
        "2.2.4. Criterios de Aceptación y Medición",
        "2.19.1. Cámaras IP",
        "2.19.2. Grabador NVR",
        "2.19.3. Televisor de Monitoreo"
    )
    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Clean-Text $p
        foreach ($h in $heading2) { if ($text.StartsWith($h)) { try { $p.Range.Style = $script:Doc.Styles.Item("Título 2") } catch {}; break } }
        foreach ($h in $heading3) { if ($text.StartsWith($h)) { try { $p.Range.Style = $script:Doc.Styles.Item("Título 3") } catch {}; break } }
    }

    for ($i = 1; $i -le $script:Doc.Tables.Count; $i++) {
        try { $script:Doc.Tables.Item($i).Rows.Item(1).HeadingFormat = $true } catch {}
    }

    foreach ($p in @($script:Doc.Paragraphs)) {
        if ((Clean-Text $p) -eq "6. CUADRO DE CANTIDADES ESTIMADAS") {
            Add-YellowNoteAfterParagraph $p "REVISAR CON EIM-GF: validar correspondencia entre los ítems del cuadro de cantidades y las partidas renumeradas del cuerpo del documento antes de emitir versión contractual."
            break
        }
    }
    Add-YellowNoteAfterTable 6 "REVISAR CON EIM-GF: completar o validar el dato de cantidad de fibras requerido para la fila OS2."
    foreach ($p in @($script:Doc.Paragraphs)) {
        if ((Clean-Text $p) -like "*Ver punto 4, para revisión de nomenclaturas.*") {
            Add-YellowNoteAfterParagraph $p "REVISAR CON EIM-GF: precisar si la referencia correcta es numeral, figura o apartado específico."
            break
        }
    }

    for ($i = $script:Doc.Paragraphs.Count; $i -ge 1; $i--) {
        $p = $script:Doc.Paragraphs.Item($i)
        if ((Clean-Text $p) -eq "/") { $p.Range.Delete() | Out-Null }
    }

    $blankRun = 0
    for ($i = $script:Doc.Paragraphs.Count; $i -ge 1; $i--) {
        $p = $script:Doc.Paragraphs.Item($i)
        $inTable = $false
        try { $inTable = [bool]$p.Range.Information(12) } catch {}
        if (-not $inTable -and (Clean-Text $p).Length -eq 0) {
            $blankRun++
            if ($blankRun -gt 1) { $p.Range.Delete() | Out-Null }
        } else {
            $blankRun = 0
        }
    }

    $script:Doc.Repaginate()
    [void]$script:Doc.Fields.Update()
    for ($si = 1; $si -le $script:Doc.Sections.Count; $si++) {
        $s = $script:Doc.Sections.Item($si)
        for ($idx = 1; $idx -le 3; $idx++) {
            try { [void]$s.Headers.Item($idx).Range.Fields.Update() } catch {}
            try { [void]$s.Footers.Item($idx).Range.Fields.Update() } catch {}
        }
    }
    $pages = $script:Doc.ComputeStatistics(2)
    Add-Log "Paginas finales segun Word: $pages"
    $script:Doc.Save()
}
finally {
    if ($script:Doc -ne $null) {
        $script:Doc.Close([ref]0) | Out-Null
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($script:Doc) | Out-Null
    }
    if ($word -ne $null) {
        $word.Quit() | Out-Null
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
    $script:Log | Set-Content -LiteralPath $LogPath -Encoding UTF8
}
