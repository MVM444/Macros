$ErrorActionPreference = "Stop"

$OriginalPath = "C:\Users\marco\Downloads\GF-EIM-IT-0000-2026-ESP_TEC-TURRIALBA-v9_final 2.docx"
$DocPath = "C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\GF-EIM-IT-0000-2026-ESP_TEC-TURRIALBA-v10_revision_editorial.docx"
$LogPath = "C:\Users\marco\OneDrive - Caja Costarricense de Seguro Social\Documentos\FreeCAD\Macros\auditoria_editorial_work\fix_cap3_numbering_log.txt"
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LogPath) | Out-Null

function Clean-Text($Paragraph) {
    return (($Paragraph.Range.Text -replace "[`r`a]", "") -replace "\s+", " ").Trim()
}

function Strip-NumPrefix([string]$Text) {
    $s = $Text
    do {
        $old = $s
        $s = ($s -replace "^\s*\d+(\.\d+)+\.?\s+", "")
    } while ($s -ne $old)
    return $s.Trim()
}

function Normalize-Key([string]$Text) {
    $s = Strip-NumPrefix $Text
    $s = $s -replace "²", "2"
    $formD = $s.Normalize([System.Text.NormalizationForm]::FormD)
    $builder = New-Object System.Text.StringBuilder
    foreach ($ch in $formD.ToCharArray()) {
        $cat = [System.Globalization.CharUnicodeInfo]::GetUnicodeCategory($ch)
        if ($cat -ne [System.Globalization.UnicodeCategory]::NonSpacingMark) {
            [void]$builder.Append($ch)
        }
    }
    return (($builder.ToString()).ToLowerInvariant() -replace "[^a-z0-9]+", "")
}

function Set-ParaText($Paragraph, [string]$Text) {
    $Paragraph.Range.Text = $Text + "`r"
}

$word = $null
$orig = $null
$doc = $null
$log = New-Object System.Collections.Generic.List[string]

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $orig = $word.Documents.Open($OriginalPath, $false, $true, $false, "", "", $false, "", "", 0, 0, $false, $false, 0, $true)
    $doc = $word.Documents.Open($DocPath, $false, $false, $false, "", "", $false, "", "", 0, 0, $false, $false, 0, $true)

    $entries = New-Object System.Collections.Generic.List[object]
    for ($i = 1; $i -le $orig.Paragraphs.Count; $i++) {
        $p = $orig.Paragraphs.Item($i)
        $num = ""
        try { $num = $p.Range.ListFormat.ListString } catch {}
        if ($num -match "^3\.(8|9)\.\d+(\.\d+)*\.$") {
            $body = Clean-Text $p
            if ($body.Length -gt 0) {
                $entries.Add([pscustomobject]@{
                    Num = $num
                    Body = $body
                    Key = Normalize-Key $body
                    IsHeading = ($p.OutlineLevel -eq 3)
                }) | Out-Null
            }
        }
    }
    $log.Add("Entradas base desde original: $($entries.Count)") | Out-Null

    $candidates = New-Object System.Collections.Generic.List[object]
    for ($i = 1; $i -le $doc.Paragraphs.Count; $i++) {
        $p = $doc.Paragraphs.Item($i)
        $text = Clean-Text $p
        $num = ""
        try { $num = $p.Range.ListFormat.ListString } catch {}
        if ($num -match "^3\.(8|9)\." -or $text -match "^\s*3\.(8|9)\.\d+") {
            $key = Normalize-Key $text
            if ($key.Length -gt 0) {
                $candidates.Add([pscustomobject]@{
                    Index = $i
                    Paragraph = $p
                    Text = $text
                    Key = $key
                    ListString = $num
                }) | Out-Null
            }
        }
    }
    $log.Add("Candidatos en copia revisada: $($candidates.Count)") | Out-Null

    $cursor = 0
    $matched = 0
    $missed = 0
    foreach ($entry in $entries) {
        $foundAt = -1
        for ($j = $cursor; $j -lt $candidates.Count; $j++) {
            if ($candidates[$j].Key -eq $entry.Key) {
                $foundAt = $j
                break
            }
        }
        if ($foundAt -lt 0) {
            for ($j = $cursor; $j -lt $candidates.Count; $j++) {
                if ($candidates[$j].Key.StartsWith($entry.Key) -or $entry.Key.StartsWith($candidates[$j].Key)) {
                    $foundAt = $j
                    break
                }
            }
        }
        if ($foundAt -lt 0) {
            $missed++
            $log.Add("No localizado: $($entry.Num) $($entry.Body)") | Out-Null
            continue
        }

        $cand = $candidates[$foundAt]
        $body = Strip-NumPrefix $cand.Text
        try { $cand.Paragraph.Range.ListFormat.RemoveNumbers() | Out-Null } catch {}
        Set-ParaText $cand.Paragraph ($entry.Num + " " + $body)
        if ($entry.IsHeading) {
            try { $cand.Paragraph.Range.Style = $doc.Styles.Item(-4) } catch {}
        }
        $matched++
        $log.Add("Corregido p$($cand.Index): $($entry.Num) $body") | Out-Null
        $cursor = $foundAt + 1
    }

    $doc.Repaginate()
    [void]$doc.Fields.Update()
    $doc.Save()
    $log.Add("Coincidencias aplicadas: $matched") | Out-Null
    $log.Add("No localizados: $missed") | Out-Null
    $log.Add("Paginas finales segun Word: $($doc.ComputeStatistics(2))") | Out-Null
}
finally {
    if ($orig -ne $null) {
        $orig.Close([ref]0) | Out-Null
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($orig) | Out-Null
    }
    if ($doc -ne $null) {
        $doc.Close([ref]0) | Out-Null
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null
    }
    if ($word -ne $null) {
        $word.Quit() | Out-Null
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
    $log | Set-Content -LiteralPath $LogPath -Encoding UTF8
}
