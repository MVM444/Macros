$ErrorActionPreference = "Stop"

$DocPath = "C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\GF-EIM-IT-0000-2026-ESP_TEC-TURRIALBA-v10_revision_editorial.docx"
$LogPath = "C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\auditoria_editorial_work\revision_editorial_log.txt"
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null
$script:Log = New-Object System.Collections.Generic.List[string]

function Add-Log([string]$Text) {
    $script:Log.Add($Text) | Out-Null
}

function Get-CleanText($Paragraph) {
    return (($Paragraph.Range.Text -replace "[`r`a]", "") -replace "\s+", " ").Trim()
}

function Set-ParagraphText($Paragraph, [string]$Text) {
    $Paragraph.Range.Text = $Text + "`r"
}

function Replace-All([string]$FindText, [string]$ReplaceText, [bool]$MatchCase = $false, [bool]$WholeWord = $false) {
    $wdFindContinue = 1
    $wdReplaceAll = 2
    $find = $script:Doc.Content.Find
    $find.ClearFormatting() | Out-Null
    $find.Replacement.ClearFormatting() | Out-Null
    [void]$find.Execute($FindText, $MatchCase, $WholeWord, $false, $false, $false, $true, $wdFindContinue, $false, $ReplaceText, $wdReplaceAll)
    Add-Log "Reemplazo: [$FindText] -> [$ReplaceText]"
}

function Add-YellowNoteAfterParagraph($Paragraph, [string]$NoteText) {
    $wdCollapseEnd = 0
    $rng = $Paragraph.Range.Duplicate
    $rng.Collapse($wdCollapseEnd) | Out-Null
    $start = $rng.Start
    $rng.InsertAfter($NoteText + "`r") | Out-Null
    $noteRange = $script:Doc.Range($start, $start + $NoteText.Length)
    $noteRange.HighlightColorIndex = 7
    $noteRange.Font.Bold = $true
    Add-Log "Nota amarilla insertada: $NoteText"
}

function Add-YellowNoteAfterTable([int]$TableIndex, [string]$NoteText) {
    $wdCollapseEnd = 0
    $table = $script:Doc.Tables.Item($TableIndex)
    $rng = $table.Range.Duplicate
    $rng.Collapse($wdCollapseEnd) | Out-Null
    $start = $rng.Start
    $rng.InsertAfter("`r" + $NoteText + "`r") | Out-Null
    $noteRange = $script:Doc.Range($start + 1, $start + 1 + $NoteText.Length)
    $noteRange.HighlightColorIndex = 7
    $noteRange.Font.Bold = $true
    Add-Log "Nota amarilla insertada tras tabla ${TableIndex}: $NoteText"
}

function Update-AllFields {
    $story = $script:Doc.StoryRanges
    foreach ($range in $story) {
        $current = $range
        while ($null -ne $current) {
            try { [void]$current.Fields.Update() } catch {}
            try { $current = $current.NextStoryRange } catch { $current = $null }
        }
    }
    Add-Log "Campos de encabezados, pies y cuerpo actualizados."
}

$word = $null
$script:Doc = $null
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3

    $script:Doc = $word.Documents.Open($DocPath, $false, $false, $false)
    $script:Doc.Repaginate()

    # Acentos y estilo editorial en titulos y textos detectados en la auditoria.
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
        @("3.1. REPOSICION DE INFRAESTRUCTURA", "3.1. REPOSICIÓN DE INFRAESTRUCTURA"),
        @("3.6. DOCUMENTACION Y OTRAS CONSIDERACIONES", "3.6. DOCUMENTACIÓN Y OTRAS CONSIDERACIONES"),
        @("3.8. ESPECIFICACIONES TECNICAS DE CABLEADO ESTRUCTURADO", "3.8. ESPECIFICACIONES TÉCNICAS DE CABLEADO ESTRUCTURADO"),
        @("3.9. ESTANDAR DE ETIQUETADO", "3.9. ESTÁNDAR DE ETIQUETADO"),
        @("4.1. ILUMINACION DE EMERGENCIA", "4.1. ILUMINACIÓN DE EMERGENCIA"),
        @("4.2. SENALIZACION DE SEGURIDAD, EVACUACION Y ACCESIBILIDAD", "4.2. SEÑALIZACIÓN DE SEGURIDAD, EVACUACIÓN Y ACCESIBILIDAD"),
        @("5.1. PRUEBAS Y VERIFICACIONES PREVIAS A LA RECEPCION PROVISIONAL", "5.1. PRUEBAS Y VERIFICACIONES PREVIAS A LA RECEPCIÓN PROVISIONAL"),
        @("5.2. DOCUMENTOS PARA LA RECEPCION PROVISIONAL", "5.2. DOCUMENTOS PARA LA RECEPCIÓN PROVISIONAL"),
        @("5.3. RECEPCION PROVISIONAL", "5.3. RECEPCIÓN PROVISIONAL"),
        @("5.4. RECEPCION DEFINITIVA", "5.4. RECEPCIÓN DEFINITIVA"),
        @("5.7. CAPACITACION AL PERSONAL", "5.7. CAPACITACIÓN AL PERSONAL"),
        @("7. SISTEMA DE EVALUACION DE OFERTAS", "7. SISTEMA DE EVALUACIÓN DE OFERTAS"),
        @("El Contratista presentara", "El Contratista presentará"),
        @("El Contratista planificara", "El Contratista planificará"),
        @(" y ejecutara ", " y ejecutará "),
        @(" quien asumirá la dirección Técnica de los trabajos. Sera", " quien asumirá la dirección Técnica de los trabajos. Será"),
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
        @("1,80m", "1,80 m")
    )
    foreach ($pair in $replacements) {
        Replace-All $pair[0] $pair[1]
    }

    # Correcciones de numeracion por parrafo para evitar reemplazos globales inseguros.
    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Get-CleanText $p
        if ($text -eq "1.16.6. Criterios de Aceptación y Medición") {
            Set-ParagraphText $p "1.16.5. Criterios de Aceptación y Medición"
            Add-Log "Renumerado 1.16.6 -> 1.16.5."
        } elseif ($text -eq "1.27.4. Normativa Aplicable") {
            Set-ParagraphText $p "1.27.3. Normativa Aplicable"
            Add-Log "Renumerado 1.27.4 -> 1.27.3."
        } elseif ($text -eq "1.27.5. Criterios de Aceptación y Forma de Medición y Pago") {
            Set-ParagraphText $p "1.27.4. Criterios de Aceptación y Forma de Medición y Pago"
            Add-Log "Renumerado 1.27.5 -> 1.27.4."
        } elseif ($text -eq "2.4. INTRODUCCIÓN A LOS REQUERIMIENTOS TÉCNICOS ELECTROMECÁNICOS") {
            Set-ParagraphText $p "INTRODUCCIÓN A LOS REQUERIMIENTOS TÉCNICOS ELECTROMECÁNICOS"
            Add-Log "Titulo introductorio de Capitulo II dejado sin numeral provisional."
        } elseif ($text -eq "2.2.4. Procedimiento Constructivo") {
            Set-ParagraphText $p "2.2.3. Procedimiento Constructivo"
            Add-Log "Renumerado 2.2.4 -> 2.2.3."
        } elseif ($text -eq "2.2.5. Criterios de Aceptación y Medición") {
            Set-ParagraphText $p "2.2.4. Criterios de Aceptación y Medición"
            Add-Log "Renumerado 2.2.5 -> 2.2.4."
        } elseif ($text -eq "2.5. DESCRIPCIÓN GENERAL DEL SISTEMA ELÉCTRICO") {
            Set-ParagraphText $p "2.3. DESCRIPCIÓN GENERAL DEL SISTEMA ELÉCTRICO"
            Add-Log "Renumerado 2.5 -> 2.3."
        } elseif ($text -eq "2.X. SISTEMA DE PUESTA A TIERRA") {
            Set-ParagraphText $p "2.4. SISTEMA DE PUESTA A TIERRA"
            Add-Log "Sustituido 2.X por 2.4."
        } elseif ($text -eq "2.X. TRANSFORMADOR DE DISTRIBUCIÓN Y ACOMETIDA") {
            Set-ParagraphText $p "2.5. TRANSFORMADOR DE DISTRIBUCIÓN Y ACOMETIDA"
            Add-Log "Sustituido 2.X por 2.5."
        } elseif ($text -eq "3. CORTINA DE AIRE EN ACCESO PRINCIPAL") {
            Set-ParagraphText $p "2.16. CORTINA DE AIRE EN ACCESO PRINCIPAL"
            Add-Log "Renumerado titulo de cortina de aire 3 -> 2.16."
        } elseif ($text -eq "2.15. SISTEMA DE ALARMA CONTRA ROBO Y SENSORES DE MOVIMIENTO") {
            Set-ParagraphText $p "2.17. SISTEMA DE ALARMA CONTRA ROBO Y SENSORES DE MOVIMIENTO"
            Add-Log "Renumerado segundo 2.15 -> 2.17."
        } elseif ($text -eq "2.16. SISTEMA DE DETECCIÓN DE INCENDIOS") {
            Set-ParagraphText $p "2.18. SISTEMA DE DETECCIÓN DE INCENDIOS"
            Add-Log "Renumerado 2.16 -> 2.18."
        } elseif ($text -eq "2.17. SISTEMA DE VIDEOVIGILANCIA") {
            Set-ParagraphText $p "2.19. SISTEMA DE VIDEOVIGILANCIA"
            Add-Log "Renumerado 2.17 -> 2.19."
        } elseif ($text -eq "2.17.1. Cámaras IP — Características Mínimas") {
            Set-ParagraphText $p "2.19.1. Cámaras IP — Características Mínimas"
            Add-Log "Renumerado 2.17.1 -> 2.19.1."
        } elseif ($text -eq "2.17.2. Grabador NVR — Características Mínimas") {
            Set-ParagraphText $p "2.19.2. Grabador NVR — Características Mínimas"
            Add-Log "Renumerado 2.17.2 -> 2.19.2."
        } elseif ($text -eq "2.17.3. Televisor de Monitoreo para Jefatura") {
            Set-ParagraphText $p "2.19.3. Televisor de Monitoreo para Jefatura"
            Add-Log "Renumerado 2.17.3 -> 2.19.3."
        } elseif ($text -eq "2.18. CONTROL DE ACCESO PARA PUERTAS DE APERTURA MANUAL MEDIANTE TARJETA RFID") {
            Set-ParagraphText $p "2.20. CONTROL DE ACCESO PARA PUERTAS DE APERTURA MANUAL MEDIANTE TARJETA RFID"
            Add-Log "Renumerado primer 2.18 -> 2.20."
        } elseif ($text -eq "2.18. BOTÓN Y ALARMA DE PÁNICO") {
            Set-ParagraphText $p "2.21. BOTÓN Y ALARMA DE PÁNICO"
            Add-Log "Renumerado segundo 2.18 -> 2.21."
        } elseif ($text -eq "2.15 RENOVACIÓN DEL SISTEMA HIDRONEUMÁTICO") {
            Set-ParagraphText $p "2.15. RENOVACIÓN DEL SISTEMA HIDRONEUMÁTICO"
            Add-Log "Normalizado punto tras 2.15."
        } elseif ($text -match "^2\.5\.(\d+)\.\s+(.*)$") {
            $n = $Matches[1]
            $rest = $Matches[2]
            Set-ParagraphText $p ("2.3." + $n + ". " + $rest)
            Add-Log "Renumerado parrafo interno 2.5.$n -> 2.3.$n."
        }
    }

    # Correccion contextual: el primer 1.20.1 bajo 1.19 debe ser 1.19.1.
    $inside119 = $false
    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Get-CleanText $p
        if ($text -like "1.19. CERRAMIENTO SUPERIOR DEL GARAJE*") {
            $inside119 = $true
            continue
        }
        if ($text -like "1.20. REPARACIÓN INTEGRAL*") {
            $inside119 = $false
        }
        if ($inside119 -and $text -eq "1.20.1. Alcance") {
            Set-ParagraphText $p "1.19.1. Alcance"
            try { $p.Range.Style = $script:Doc.Styles.Item("Título 3") } catch {}
            Add-Log "Renumerado y reestilizado 1.20.1 bajo 1.19 -> 1.19.1."
            $inside119 = $false
        }
    }

    # Convertir listas internas que colisionaban con la jerarquia en vinetas.
    foreach ($p in @($script:Doc.Paragraphs)) {
        $listString = ""
        try { $listString = $p.Range.ListFormat.ListString } catch {}
        if ($listString -match "^3\.6\.[1-7]\.$" -or $listString -match "^3\.7\.(2|3|4|5|6|7|8|9|10)\.$") {
            try {
                $p.Range.ListFormat.ApplyBulletDefault() | Out-Null
                Add-Log "Lista interna convertida a vineta: $listString"
            } catch {}
        }
    }

    # Convertir numeros automaticos de titulos a texto estable para uniformidad visual.
    foreach ($p in @($script:Doc.Paragraphs)) {
        $styleName = ""
        $listString = ""
        try { $styleName = $p.Range.Style.NameLocal } catch {}
        try { $listString = $p.Range.ListFormat.ListString } catch {}
        if ($styleName -like "Título 3*" -and $listString -match "^\d+\.\d+\.\d+\.$") {
            try {
                $p.Range.ListFormat.ConvertNumbersToText() | Out-Null
                Add-Log "Numero automatico de titulo convertido a texto: $listString"
            } catch {}
        }
    }

    # Corregir estilo de parrafos de cuerpo que estaban marcados como titulos.
    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Get-CleanText $p
        if ($text.Length -eq 0) { continue }
        $styleName = ""
        $listString = ""
        try { $styleName = $p.Range.Style.NameLocal } catch {}
        try { $listString = $p.Range.ListFormat.ListString } catch {}
        if (($styleName -like "Título 3*" -or $styleName -like "Título 4*") -and
            $text -notmatch "^\d+(\.\d+)*\.?\s+" -and
            $listString -notmatch "^\d+\.\d+\.\d+\.$" -and
            $text.Length -gt 70) {
            try {
                $p.Range.Style = $script:Doc.Styles.Item("Normal")
                Add-Log "Parrafo de cuerpo reestilizado como Normal: $($text.Substring(0, [Math]::Min(80, $text.Length)))"
            } catch {}
        }
    }

    # Repetir encabezado en tablas y limpiar espaciados manuales excesivos.
    for ($i = 1; $i -le $script:Doc.Tables.Count; $i++) {
        try { $script:Doc.Tables.Item($i).Rows.Item(1).HeadingFormat = $true } catch {}
    }
    Add-Log "Encabezado repetible activado en tablas cuando Word lo permitio."

    # Notas amarillas donde se requiere criterio tecnico/contractual.
    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Get-CleanText $p
        if ($text -eq "6. CUADRO DE CANTIDADES ESTIMADAS") {
            Add-YellowNoteAfterParagraph $p "REVISAR CON EIM-GF: validar correspondencia entre los ítems del cuadro de cantidades y las partidas renumeradas del cuerpo del documento antes de emitir versión contractual."
            break
        }
    }
    Add-YellowNoteAfterTable 6 "REVISAR CON EIM-GF: completar o validar el dato de cantidad de fibras requerido para la fila OS2."
    foreach ($p in @($script:Doc.Paragraphs)) {
        $text = Get-CleanText $p
        if ($text -like "*Ver punto 4, para revisión de nomenclaturas.*") {
            Add-YellowNoteAfterParagraph $p "REVISAR CON EIM-GF: precisar si la referencia correcta es numeral, figura o apartado específico."
            break
        }
    }

    # Eliminar parrafos residuales con barra sola.
    for ($i = $script:Doc.Paragraphs.Count; $i -ge 1; $i--) {
        $p = $script:Doc.Paragraphs.Item($i)
        $text = Get-CleanText $p
        if ($text -eq "/") {
            $p.Range.Delete() | Out-Null
            Add-Log "Eliminado parrafo residual con barra sola."
        }
    }

    # Reducir corridas de parrafos vacios fuera de tablas a un solo parrafo.
    $blankRun = 0
    for ($i = $script:Doc.Paragraphs.Count; $i -ge 1; $i--) {
        $p = $script:Doc.Paragraphs.Item($i)
        $text = Get-CleanText $p
        $inTable = $false
        try { $inTable = [bool]$p.Range.Information(12) } catch {}
        if (-not $inTable -and $text.Length -eq 0) {
            $blankRun++
            if ($blankRun -gt 1) {
                $p.Range.Delete() | Out-Null
                Add-Log "Eliminado parrafo vacio repetido."
            }
        } else {
            $blankRun = 0
        }
    }

    Update-AllFields
    $script:Doc.Repaginate()
    $script:Doc.Save()
    Add-Log "Documento guardado: $DocPath"
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
