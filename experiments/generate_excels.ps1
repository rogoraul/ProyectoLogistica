Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$InvariantCulture = [System.Globalization.CultureInfo]::InvariantCulture

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$ExperimentsDir = Join-Path $ProjectRoot "experiments"
$OutputDir = Join-Path $ProjectRoot "output\spreadsheet"
$TempRoot = Join-Path $ProjectRoot "tmp\spreadsheets"

$CalibrationSummaryPath = Join-Path $ExperimentsDir "calibration_summary.json"
$GraspDetailPath = Join-Path $ExperimentsDir "calibration_grasp.csv"
$GraspSummaryPath = Join-Path $ExperimentsDir "calibration_grasp_summary.csv"
$GraspRunsPath = Join-Path $ExperimentsDir "calibration_grasp_runs.csv"
$TsDetailPath = Join-Path $ExperimentsDir "calibration_ts.csv"
$TsSummaryPath = Join-Path $ExperimentsDir "calibration_ts_summary.csv"
$TsRunsPath = Join-Path $ExperimentsDir "calibration_ts_runs.csv"
$ComparisonResultsPath = Join-Path $ExperimentsDir "comparison_results.csv"
$ComparisonRunsPath = Join-Path $ExperimentsDir "comparison_runs.csv"
$ComparisonTestsPath = Join-Path $ExperimentsDir "comparison_tests.json"

$GraspWorkbookPath = Join-Path $OutputDir "calibracion_grasp.xlsx"
$TsWorkbookPath = Join-Path $OutputDir "calibracion_ts.xlsx"
$ComparisonWorkbookPath = Join-Path $OutputDir "comparacion_final.xlsx"
$UnifiedWorkbookPath = Join-Path $OutputDir "experimentacion_completa.xlsx"

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Get-FullPath {
    param([string]$Path)
    [System.IO.Path]::GetFullPath($Path)
}

function Assert-PathUnderRoot {
    param([string]$Path, [string]$Root)
    $fullPath = Get-FullPath $Path
    $fullRoot = Get-FullPath $Root
    if (-not $fullPath.StartsWith($fullRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe path operation outside of allowed root: $fullPath"
    }
}

function Remove-SafeItem {
    param([string]$Path, [string]$AllowedRoot, [switch]$Recurse)
    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    Assert-PathUnderRoot -Path $Path -Root $AllowedRoot
    if ($Recurse) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
    else {
        Remove-Item -LiteralPath $Path -Force
    }
}

function Write-Utf8File {
    param([string]$Path, [string]$Content)
    $directory = Split-Path -Parent $Path
    if ($directory) {
        Ensure-Directory $directory
    }
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Escape-Xml {
    param([AllowNull()][object]$Text)
    if ($null -eq $Text) {
        return ""
    }
    [System.Security.SecurityElement]::Escape([string]$Text)
}

function ConvertTo-ColumnName {
    param([int]$Index)
    $value = $Index
    $name = ""
    while ($value -gt 0) {
        $remainder = ($value - 1) % 26
        $name = [char](65 + $remainder) + $name
        $value = [math]::Floor(($value - 1) / 26)
    }
    $name
}

function Get-CellReference {
    param([int]$Row, [int]$Column)
    "{0}{1}" -f (ConvertTo-ColumnName $Column), $Row
}

function New-TextCell {
    param([AllowNull()][object]$Value, [int]$Style = 4)
    [pscustomobject]@{
        kind    = "text"
        value   = if ($null -eq $Value) { "" } else { [string]$Value }
        style   = $Style
        display = if ($null -eq $Value) { "" } else { [string]$Value }
    }
}

function New-NumberCell {
    param([AllowNull()][object]$Value, [int]$Style = 5, [string]$Display = "")
    if ($null -eq $Value -or [string]::IsNullOrWhiteSpace([string]$Value)) {
        return New-TextCell -Value "" -Style 4
    }
    $number = [double]::Parse([string]$Value, $InvariantCulture)
    $displayValue = if ($Display) { $Display } else { $number.ToString($InvariantCulture) }
    [pscustomobject]@{
        kind    = "number"
        value   = $number.ToString($InvariantCulture)
        style   = $Style
        display = $displayValue
    }
}

function New-IntegerCell {
    param([AllowNull()][object]$Value, [int]$Style = 8, [string]$Display = "")
    if ($null -eq $Value -or [string]::IsNullOrWhiteSpace([string]$Value)) {
        return New-TextCell -Value "" -Style 4
    }
    $number = [int]::Parse([string]$Value, $InvariantCulture)
    $displayValue = if ($Display) { $Display } else { $number.ToString($InvariantCulture) }
    [pscustomobject]@{
        kind    = "number"
        value   = $number.ToString($InvariantCulture)
        style   = $Style
        display = $displayValue
    }
}

function New-FormulaCell {
    param([string]$Formula, [int]$Style = 5, [string]$Display = "")
    [pscustomobject]@{
        kind    = "formula"
        formula = $Formula
        style   = $Style
        display = $Display
    }
}

function New-CellFromValue {
    param([AllowNull()][object]$Value, [string]$Type, [bool]$Highlight = $false)
    switch ($Type) {
        "text" { return New-TextCell -Value $Value -Style $(if ($Highlight) { 9 } else { 4 }) }
        "number2" { return New-NumberCell -Value $Value -Style $(if ($Highlight) { 10 } else { 5 }) }
        "number3" { return New-NumberCell -Value $Value -Style $(if ($Highlight) { 11 } else { 6 }) }
        "percent" { return New-NumberCell -Value $Value -Style $(if ($Highlight) { 12 } else { 7 }) }
        "int" { return New-IntegerCell -Value $Value -Style $(if ($Highlight) { 13 } else { 8 }) }
        "number6" { return New-NumberCell -Value $Value -Style $(if ($Highlight) { 15 } else { 14 }) }
        default { throw "Unsupported cell type: $Type" }
    }
}

function Add-Row {
    param([System.Collections.Generic.List[object]]$Rows, [object[]]$Cells)
    $Rows.Add($Cells) | Out-Null
}

function New-Sheet {
    param([string]$Name, [System.Collections.Generic.List[object]]$Rows, [string]$FreezeCell = "", [bool]$AutoFilter = $false)
    [pscustomobject]@{
        Name       = $Name
        Rows       = $Rows
        FreezeCell = $FreezeCell
        AutoFilter = $AutoFilter
    }
}

function Build-TableRows {
    param([System.Collections.IEnumerable]$Objects, [array]$Columns, [scriptblock]$HighlightBlock = $null)
    $rows = [System.Collections.Generic.List[object]]::new()
    $headerCells = [System.Collections.Generic.List[object]]::new()
    foreach ($column in $Columns) {
        $headerCells.Add((New-TextCell -Value $column.header -Style 2)) | Out-Null
    }
    Add-Row -Rows $rows -Cells $headerCells.ToArray()
    foreach ($item in $Objects) {
        $highlight = $false
        if ($null -ne $HighlightBlock) {
            $highlight = [bool](& $HighlightBlock $item)
        }
        $cells = [System.Collections.Generic.List[object]]::new()
        foreach ($column in $Columns) {
            $rawValue = if ($column.Contains("expr")) { & $column.expr $item } else { $item.($column.key) }
            if ($rawValue -is [pscustomobject] -and $rawValue.PSObject.Properties.Match("kind").Count -gt 0) {
                $cells.Add($rawValue) | Out-Null
            }
            else {
                $cells.Add((New-CellFromValue -Value $rawValue -Type $column.type -Highlight $highlight)) | Out-Null
            }
        }
        Add-Row -Rows $rows -Cells $cells.ToArray()
    }
    $rows
}

function Get-CellDisplayText {
    param([object]$Cell)
    if ($null -eq $Cell) { return "" }
    if ($Cell.PSObject.Properties.Match("display").Count -gt 0 -and $Cell.display) { return [string]$Cell.display }
    if ($Cell.kind -eq "formula") { return "" }
    [string]$Cell.value
}

function Measure-ColumnWidths {
    param([System.Collections.Generic.List[object]]$Rows)
    $maxColumns = 1
    foreach ($row in $Rows) {
        if ($row.Count -gt $maxColumns) { $maxColumns = $row.Count }
    }
    $widths = @()
    for ($colIndex = 1; $colIndex -le $maxColumns; $colIndex++) {
        $maxLength = 10
        foreach ($row in $Rows) {
            if ($row.Count -lt $colIndex) { continue }
            $text = Get-CellDisplayText -Cell $row[$colIndex - 1]
            if ($text.Length -gt $maxLength) { $maxLength = $text.Length }
        }
        $widths += [math]::Min([math]::Max($maxLength + 2, 10), 80)
    }
    $widths
}

function Get-FreezeXml {
    param([string]$FreezeCell)
    if ([string]::IsNullOrWhiteSpace($FreezeCell)) { return "" }
    if ($FreezeCell -match "^([A-Z]+)(\d+)$") {
        $letters = $Matches[1]
        $rowNumber = [int]$Matches[2]
        $columnNumber = 0
        foreach ($letter in $letters.ToCharArray()) {
            $columnNumber = ($columnNumber * 26) + ([int][char]$letter - 64)
        }
        $xSplit = [math]::Max($columnNumber - 1, 0)
        $ySplit = [math]::Max($rowNumber - 1, 0)
        if ($xSplit -eq 0 -and $ySplit -eq 0) { return "" }
        $activePane = if ($xSplit -gt 0 -and $ySplit -gt 0) { "bottomRight" } elseif ($xSplit -gt 0) { "topRight" } else { "bottomLeft" }
        $attributes = @()
        if ($xSplit -gt 0) { $attributes += "xSplit=`"$xSplit`"" }
        if ($ySplit -gt 0) { $attributes += "ySplit=`"$ySplit`"" }
        $attributes += "topLeftCell=`"$FreezeCell`""
        $attributes += "activePane=`"$activePane`""
        $attributes += "state=`"frozen`""
        return "<sheetViews><sheetView workbookViewId=`"0`"><pane {0}/></sheetView></sheetViews>" -f ($attributes -join " ")
    }
    throw "Unsupported freeze cell reference: $FreezeCell"
}

function Get-WorksheetXml {
    param([pscustomobject]$Sheet)
    $rowCount = [math]::Max($Sheet.Rows.Count, 1)
    $maxColumns = 1
    foreach ($row in $Sheet.Rows) {
        if ($row.Count -gt $maxColumns) { $maxColumns = $row.Count }
    }
    $lastColumn = ConvertTo-ColumnName $maxColumns
    $dimension = "A1:{0}{1}" -f $lastColumn, $rowCount
    $widths = Measure-ColumnWidths -Rows $Sheet.Rows
    $sheetViewsXml = Get-FreezeXml -FreezeCell $Sheet.FreezeCell
    $colsBuilder = New-Object System.Text.StringBuilder
    if ($widths.Count -gt 0) {
        [void]$colsBuilder.Append("<cols>")
        for ($i = 0; $i -lt $widths.Count; $i++) {
            [void]$colsBuilder.Append(("<col min=`"{0}`" max=`"{0}`" width=`"{1}`" customWidth=`"1`"/>" -f ($i + 1), $widths[$i].ToString($InvariantCulture)))
        }
        [void]$colsBuilder.Append("</cols>")
    }
    $rowsBuilder = New-Object System.Text.StringBuilder
    for ($rowIndex = 0; $rowIndex -lt $Sheet.Rows.Count; $rowIndex++) {
        $excelRow = $rowIndex + 1
        $row = $Sheet.Rows[$rowIndex]
        [void]$rowsBuilder.Append("<row r=`"$excelRow`">")
        for ($colIndex = 0; $colIndex -lt $row.Count; $colIndex++) {
            $cell = $row[$colIndex]
            $cellRef = Get-CellReference -Row $excelRow -Column ($colIndex + 1)
            switch ($cell.kind) {
                "text" {
                    $text = Escape-Xml $cell.value
                    [void]$rowsBuilder.Append("<c r=`"$cellRef`" s=`"$($cell.style)`" t=`"inlineStr`"><is><t xml:space=`"preserve`">$text</t></is></c>")
                }
                "number" {
                    [void]$rowsBuilder.Append("<c r=`"$cellRef`" s=`"$($cell.style)`"><v>$($cell.value)</v></c>")
                }
                "formula" {
                    $formula = Escape-Xml $cell.formula
                    [void]$rowsBuilder.Append("<c r=`"$cellRef`" s=`"$($cell.style)`"><f>$formula</f></c>")
                }
                default {
                    throw "Unsupported cell kind: $($cell.kind)"
                }
            }
        }
        [void]$rowsBuilder.Append("</row>")
    }
    if ($Sheet.Rows.Count -eq 0) { [void]$rowsBuilder.Append("<row r=`"1`"/>") }
    $autoFilterXml = ""
    if ($Sheet.AutoFilter -and $Sheet.Rows.Count -ge 1 -and $maxColumns -ge 1) {
        $autoFilterXml = "<autoFilter ref=`"A1:{0}{1}`"/>" -f $lastColumn, $Sheet.Rows.Count
    }
    @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <dimension ref="$dimension"/>
  $sheetViewsXml
  $($colsBuilder.ToString())
  <sheetFormatPr defaultRowHeight="15"/>
  <sheetData>
    $($rowsBuilder.ToString())
  </sheetData>
  $autoFilterXml
</worksheet>
"@
}

function Get-StylesXml {
    @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="5">
    <numFmt numFmtId="164" formatCode="0.00"/>
    <numFmt numFmtId="165" formatCode="0.000"/>
    <numFmt numFmtId="166" formatCode="0.0000\%"/>
    <numFmt numFmtId="167" formatCode="0"/>
    <numFmt numFmtId="168" formatCode="0.000000"/>
  </numFmts>
  <fonts count="4">
    <font><sz val="11"/><color rgb="FF000000"/><name val="Calibri"/><family val="2"/></font>
    <font><b/><sz val="14"/><color rgb="FF1F1F1F"/><name val="Calibri"/><family val="2"/></font>
    <font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/><family val="2"/></font>
    <font><b/><sz val="11"/><color rgb="FF1F1F1F"/><name val="Calibri"/><family val="2"/></font>
  </fonts>
  <fills count="5">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF2F5496"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE2EFDA"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFD9EAF7"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color auto="1"/></left>
      <right style="thin"><color auto="1"/></right>
      <top style="thin"><color auto="1"/></top>
      <bottom style="thin"><color auto="1"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="16">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>
    <xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1"/>
    <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyBorder="1"/>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
    <xf numFmtId="165" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
    <xf numFmtId="166" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
    <xf numFmtId="167" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
    <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFill="1" applyBorder="1"/>
    <xf numFmtId="164" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>
    <xf numFmtId="165" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>
    <xf numFmtId="166" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>
    <xf numFmtId="167" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>
    <xf numFmtId="168" fontId="0" fillId="0" borderId="1" xfId="0" applyNumberFormat="1" applyBorder="1"/>
    <xf numFmtId="168" fontId="0" fillId="3" borderId="1" xfId="0" applyNumberFormat="1" applyFill="1" applyBorder="1"/>
  </cellXfs>
  <cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>
</styleSheet>
'@
}

function Get-WorkbookXml {
    param([array]$Sheets)
    $sheetsBuilder = New-Object System.Text.StringBuilder
    for ($i = 0; $i -lt $Sheets.Count; $i++) {
        $sheetName = Escape-Xml $Sheets[$i].Name
        [void]$sheetsBuilder.Append(("<sheet name=`"$sheetName`" sheetId=`"{0}`" r:id=`"rId{0}`"/>" -f ($i + 1)))
    }
    @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <bookViews><workbookView xWindow="0" yWindow="0" windowWidth="24000" windowHeight="12000"/></bookViews>
  <sheets>$($sheetsBuilder.ToString())</sheets>
  <calcPr calcId="191029" fullCalcOnLoad="1"/>
</workbook>
"@
}

function Get-WorkbookRelsXml {
    param([array]$Sheets)
    $relsBuilder = New-Object System.Text.StringBuilder
    for ($i = 0; $i -lt $Sheets.Count; $i++) {
        [void]$relsBuilder.Append(("<Relationship Id=`"rId{0}`" Type=`"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet`" Target=`"worksheets/sheet{0}.xml`"/>" -f ($i + 1)))
    }
    $styleRelId = $Sheets.Count + 1
    [void]$relsBuilder.Append("<Relationship Id=`"rId$styleRelId`" Type=`"http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles`" Target=`"styles.xml`"/>")
    @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  $($relsBuilder.ToString())
</Relationships>
"@
}

function Get-RootRelsXml {
    @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
'@
}

function Get-ContentTypesXml {
    param([array]$Sheets)
    $overridesBuilder = New-Object System.Text.StringBuilder
    for ($i = 0; $i -lt $Sheets.Count; $i++) {
        [void]$overridesBuilder.Append(("<Override PartName=`"/xl/worksheets/sheet{0}.xml`" ContentType=`"application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml`"/>" -f ($i + 1)))
    }
    @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  $($overridesBuilder.ToString())
</Types>
"@
}

function Get-CoreXml {
    param([string]$Title, [string]$Author)
    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ", $InvariantCulture)
    @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>$(Escape-Xml $Title)</dc:title>
  <dc:creator>$(Escape-Xml $Author)</dc:creator>
  <cp:lastModifiedBy>$(Escape-Xml $Author)</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">$timestamp</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">$timestamp</dcterms:modified>
</cp:coreProperties>
"@
}

function Get-AppXml {
    param([array]$Sheets)
    $titlesBuilder = New-Object System.Text.StringBuilder
    foreach ($sheet in $Sheets) {
        [void]$titlesBuilder.Append(("<vt:lpstr>{0}</vt:lpstr>" -f (Escape-Xml $sheet.Name)))
    }
    @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex Spreadsheet Export</Application>
  <HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>$($Sheets.Count)</vt:i4></vt:variant></vt:vector></HeadingPairs>
  <TitlesOfParts><vt:vector size="$($Sheets.Count)" baseType="lpstr">$($titlesBuilder.ToString())</vt:vector></TitlesOfParts>
  <Company></Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0300</AppVersion>
</Properties>
"@
}

function Write-XlsxWorkbook {
    param([string]$OutputPath, [string]$Title, [array]$Sheets)
    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    Ensure-Directory $OutputDir
    Ensure-Directory $TempRoot
    $workDir = Join-Path $TempRoot ([System.IO.Path]::GetFileNameWithoutExtension($OutputPath))
    $zipPath = "$workDir.zip"
    Remove-SafeItem -Path $workDir -AllowedRoot $TempRoot -Recurse
    Remove-SafeItem -Path $zipPath -AllowedRoot $TempRoot
    Remove-SafeItem -Path $OutputPath -AllowedRoot $OutputDir
    Ensure-Directory $workDir
    Ensure-Directory (Join-Path $workDir "_rels")
    Ensure-Directory (Join-Path $workDir "docProps")
    Ensure-Directory (Join-Path $workDir "xl")
    Ensure-Directory (Join-Path $workDir "xl\_rels")
    Ensure-Directory (Join-Path $workDir "xl\worksheets")
    Write-Utf8File -Path (Join-Path $workDir "[Content_Types].xml") -Content (Get-ContentTypesXml -Sheets $Sheets)
    Write-Utf8File -Path (Join-Path $workDir "_rels\.rels") -Content (Get-RootRelsXml)
    Write-Utf8File -Path (Join-Path $workDir "docProps\core.xml") -Content (Get-CoreXml -Title $Title -Author "Codex")
    Write-Utf8File -Path (Join-Path $workDir "docProps\app.xml") -Content (Get-AppXml -Sheets $Sheets)
    Write-Utf8File -Path (Join-Path $workDir "xl\workbook.xml") -Content (Get-WorkbookXml -Sheets $Sheets)
    Write-Utf8File -Path (Join-Path $workDir "xl\_rels\workbook.xml.rels") -Content (Get-WorkbookRelsXml -Sheets $Sheets)
    Write-Utf8File -Path (Join-Path $workDir "xl\styles.xml") -Content (Get-StylesXml)
    for ($i = 0; $i -lt $Sheets.Count; $i++) {
        $sheetPath = Join-Path $workDir ("xl\worksheets\sheet{0}.xml" -f ($i + 1))
        Write-Utf8File -Path $sheetPath -Content (Get-WorksheetXml -Sheet $Sheets[$i])
    }
    $zipStream = [System.IO.File]::Open($zipPath, [System.IO.FileMode]::CreateNew)
    $archive = New-Object System.IO.Compression.ZipArchive($zipStream, [System.IO.Compression.ZipArchiveMode]::Create, $false)
    try {
        foreach ($file in (Get-ChildItem -LiteralPath $workDir -Recurse -File)) {
            $relativePath = $file.FullName.Substring($workDir.Length).TrimStart('\', '/')
            $entryName = $relativePath -replace '\\', '/'
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile($archive, $file.FullName, $entryName, [System.IO.Compression.CompressionLevel]::Optimal) | Out-Null
        }
    }
    finally {
        $archive.Dispose()
        $zipStream.Dispose()
    }
    Move-Item -LiteralPath $zipPath -Destination $OutputPath -Force
    Remove-SafeItem -Path $workDir -AllowedRoot $TempRoot -Recurse
}

function Get-SourceRowsInfo {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return "-" }
    if ([System.IO.Path]::GetExtension($Path).ToLowerInvariant() -eq ".csv") {
        return (Import-Csv -LiteralPath $Path).Count
    }
    "-"
}

function Build-SourcesSheet {
    param([array]$SourcePaths)
    $items = foreach ($entry in $SourcePaths) {
        $item = Get-Item -LiteralPath $entry.path
        [pscustomobject]@{
            role = $entry.role
            path = Get-FullPath $item.FullName
            rows = Get-SourceRowsInfo -Path $item.FullName
            modified = $item.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss", $InvariantCulture)
        }
    }
    $columns = @(
        @{ header = "Rol"; key = "role"; type = "text" },
        @{ header = "Ruta"; key = "path"; type = "text" },
        @{ header = "Filas"; key = "rows"; type = "text" },
        @{ header = "Ultima modificacion"; key = "modified"; type = "text" }
    )
    New-Sheet -Name "Fuentes" -Rows (Build-TableRows -Objects $items -Columns $columns) -FreezeCell "A2" -AutoFilter $true
}

function Build-GraspWorkbookSheets {
    param([array]$GraspDetail, [array]$GraspSummary, [array]$GraspRuns, [pscustomobject]$CalibrationSummary)
    $bestByGroup = @{}
    foreach ($row in $GraspSummary) {
        $group = $row.group
        $dev = [double]::Parse($row.avg_dev_pct, $InvariantCulture)
        if (-not $bestByGroup.ContainsKey($group) -or $dev -lt $bestByGroup[$group]) {
            $bestByGroup[$group] = $dev
        }
    }
    $summaryRows = [System.Collections.Generic.List[object]]::new()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Calibracion GRASP" -Style 1))
    Add-Row -Rows $summaryRows -Cells @()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Metadato" -Style 2), (New-TextCell -Value "Valor" -Style 2))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Fecha generacion calibracion" -Style 3), (New-TextCell -Value $CalibrationSummary.generated_at -Style 4))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Time limit por configuracion (s)" -Style 3), (New-IntegerCell -Value $CalibrationSummary.time_limit_s -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Runs por configuracion" -Style 3), (New-IntegerCell -Value $CalibrationSummary.runs_per_config -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Alpha values explorados" -Style 3), (New-TextCell -Value (($CalibrationSummary.alpha_values | ForEach-Object { $_.ToString() }) -join ", ") -Style 4))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Configuraciones resumidas" -Style 3), (New-FormulaCell -Formula ("COUNTA('Resumen alpha'!A2:A{0})" -f ($GraspSummary.Count + 1)) -Style 8 -Display $GraspSummary.Count.ToString($InvariantCulture)))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Runs almacenados" -Style 3), (New-FormulaCell -Formula ("COUNTA(Runs!A2:A{0})" -f ($GraspRuns.Count + 1)) -Style 8 -Display $GraspRuns.Count.ToString($InvariantCulture)))
    Add-Row -Rows $summaryRows -Cells @()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Mejores parametros por grupo" -Style 1))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Grupo" -Style 2), (New-TextCell -Value "Etiqueta" -Style 2), (New-TextCell -Value "Mejor alpha" -Style 2), (New-TextCell -Value "Best avg dev%" -Style 2))
    foreach ($groupName in @("small", "large")) {
        $groupInfo = $CalibrationSummary.groups.$groupName
        Add-Row -Rows $summaryRows -Cells @(
            (New-TextCell -Value $groupName -Style 4),
            (New-TextCell -Value $groupInfo.label -Style 4),
            (New-NumberCell -Value $groupInfo.grasp.best_alpha -Style 11),
            (New-NumberCell -Value $groupInfo.grasp.best_avg_dev_pct -Style 12)
        )
    }
    $summaryColumns = @(
        @{ header = "Grupo"; key = "group"; type = "text" },
        @{ header = "Alpha"; key = "alpha"; type = "number3" },
        @{ header = "Avg dev%"; key = "avg_dev_pct"; type = "percent" },
        @{ header = "Mean avg OF"; key = "mean_avg_of"; type = "number2" },
        @{ header = "Mean time (s)"; key = "mean_time_s"; type = "number3" },
        @{ header = "Seleccionado"; expr = { param($row) if ([double]::Parse($row.avg_dev_pct, $InvariantCulture) -eq $bestByGroup[$row.group]) { "si" } else { "" } }; type = "text" }
    )
    $detailColumns = @(
        @{ header = "Grupo"; key = "group"; type = "text" },
        @{ header = "Instancia"; key = "instance"; type = "text" },
        @{ header = "Alpha"; key = "alpha"; type = "number3" },
        @{ header = "Avg OF"; key = "avg_of"; type = "number2" },
        @{ header = "Best OF"; key = "best_of"; type = "number2" },
        @{ header = "Worst OF"; key = "worst_of"; type = "number2" },
        @{ header = "Std OF"; key = "std_of"; type = "number2" },
        @{ header = "Avg time (s)"; key = "avg_time_s"; type = "number3" },
        @{ header = "Avg dev%"; key = "avg_dev_pct"; type = "percent" }
    )
    $runsColumns = @(
        @{ header = "Grupo"; key = "group"; type = "text" },
        @{ header = "Instancia"; key = "instance"; type = "text" },
        @{ header = "Alpha"; key = "alpha"; type = "number3" },
        @{ header = "Run"; key = "run"; type = "int" },
        @{ header = "Seed"; key = "seed"; type = "int" },
        @{ header = "OF"; key = "of"; type = "number2" },
        @{ header = "Tiempo (s)"; key = "elapsed_s"; type = "number3" }
    )
    @(
        (New-Sheet -Name "Resumen" -Rows $summaryRows),
        (New-Sheet -Name "Resumen alpha" -Rows (Build-TableRows -Objects $GraspSummary -Columns $summaryColumns -HighlightBlock { param($row) [double]::Parse($row.avg_dev_pct, $InvariantCulture) -eq $bestByGroup[$row.group] }) -FreezeCell "A2" -AutoFilter $true),
        (New-Sheet -Name "Detalle instancias" -Rows (Build-TableRows -Objects $GraspDetail -Columns $detailColumns) -FreezeCell "A2" -AutoFilter $true),
        (New-Sheet -Name "Runs" -Rows (Build-TableRows -Objects $GraspRuns -Columns $runsColumns) -FreezeCell "A2" -AutoFilter $true),
        (Build-SourcesSheet -SourcePaths @(
            @{ role = "JSON resumen"; path = $CalibrationSummaryPath },
            @{ role = "CSV detalle"; path = $GraspDetailPath },
            @{ role = "CSV resumen"; path = $GraspSummaryPath },
            @{ role = "CSV runs"; path = $GraspRunsPath }
        ))
    )
}

function Build-TsWorkbookSheets {
    param([array]$TsDetail, [array]$TsSummary, [array]$TsRuns, [pscustomobject]$CalibrationSummary)
    $bestByGroupPhase = @{}
    foreach ($row in $TsSummary) {
        $key = "{0}|{1}" -f $row.group, $row.phase
        $dev = [double]::Parse($row.avg_dev_pct, $InvariantCulture)
        if (-not $bestByGroupPhase.ContainsKey($key) -or $dev -lt $bestByGroupPhase[$key]) {
            $bestByGroupPhase[$key] = $dev
        }
    }
    $summaryRows = [System.Collections.Generic.List[object]]::new()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Calibracion GRASP + TS" -Style 1))
    Add-Row -Rows $summaryRows -Cells @()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Metadato" -Style 2), (New-TextCell -Value "Valor" -Style 2))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Fecha generacion calibracion" -Style 3), (New-TextCell -Value $CalibrationSummary.generated_at -Style 4))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Modo" -Style 3), (New-TextCell -Value $CalibrationSummary.mode -Style 4))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Time limit por configuracion (s)" -Style 3), (New-IntegerCell -Value $CalibrationSummary.time_limit_s -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Runs por configuracion" -Style 3), (New-IntegerCell -Value $CalibrationSummary.runs_per_config -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Alpha values explorados" -Style 3), (New-TextCell -Value (($CalibrationSummary.alpha_values | ForEach-Object { $_.ToString() }) -join ", ") -Style 4))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Tenure values explorados" -Style 3), (New-TextCell -Value (($CalibrationSummary.tenure_values | ForEach-Object { $_.ToString() }) -join ", ") -Style 4))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Anchor tenure alpha sweep" -Style 3), (New-IntegerCell -Value $CalibrationSummary.alpha_sweep_tenure -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Configuraciones resumidas" -Style 3), (New-FormulaCell -Formula ("COUNTA('Resumen configuraciones'!A2:A{0})" -f ($TsSummary.Count + 1)) -Style 8 -Display $TsSummary.Count.ToString($InvariantCulture)))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Runs almacenados" -Style 3), (New-FormulaCell -Formula ("COUNTA(Runs!A2:A{0})" -f ($TsRuns.Count + 1)) -Style 8 -Display $TsRuns.Count.ToString($InvariantCulture)))
    Add-Row -Rows $summaryRows -Cells @()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Mejores parametros por grupo" -Style 1))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Grupo" -Style 2), (New-TextCell -Value "Etiqueta" -Style 2), (New-TextCell -Value "Best alpha" -Style 2), (New-TextCell -Value "Best tenure" -Style 2), (New-TextCell -Value "Best avg dev%" -Style 2))
    foreach ($groupName in @("small", "large")) {
        $groupInfo = $CalibrationSummary.groups.$groupName
        Add-Row -Rows $summaryRows -Cells @(
            (New-TextCell -Value $groupName -Style 4),
            (New-TextCell -Value $groupInfo.label -Style 4),
            (New-NumberCell -Value $groupInfo.ts.best_alpha -Style 11),
            (New-IntegerCell -Value $groupInfo.ts.best_tenure -Style 13),
            (New-NumberCell -Value $groupInfo.ts.best_avg_dev_pct -Style 12)
        )
    }
    $summaryColumns = @(
        @{ header = "Grupo"; key = "group"; type = "text" },
        @{ header = "Fase"; key = "phase"; type = "text" },
        @{ header = "Alpha"; key = "alpha"; type = "number3" },
        @{ header = "Tenure"; key = "tenure"; type = "int" },
        @{ header = "Avg dev%"; key = "avg_dev_pct"; type = "percent" },
        @{ header = "Mean avg OF"; key = "mean_avg_of"; type = "number2" },
        @{ header = "Mean time (s)"; key = "mean_time_s"; type = "number3" },
        @{ header = "Seleccionado"; expr = { param($row) $key = "{0}|{1}" -f $row.group, $row.phase; if ([double]::Parse($row.avg_dev_pct, $InvariantCulture) -eq $bestByGroupPhase[$key]) { "si" } else { "" } }; type = "text" }
    )
    $detailColumns = @(
        @{ header = "Grupo"; key = "group"; type = "text" },
        @{ header = "Fase"; key = "phase"; type = "text" },
        @{ header = "Instancia"; key = "instance"; type = "text" },
        @{ header = "Alpha"; key = "alpha"; type = "number3" },
        @{ header = "Tenure"; key = "tenure"; type = "int" },
        @{ header = "Avg OF"; key = "avg_of"; type = "number2" },
        @{ header = "Best OF"; key = "best_of"; type = "number2" },
        @{ header = "Worst OF"; key = "worst_of"; type = "number2" },
        @{ header = "Std OF"; key = "std_of"; type = "number2" },
        @{ header = "Avg time (s)"; key = "avg_time_s"; type = "number3" },
        @{ header = "Avg dev%"; key = "avg_dev_pct"; type = "percent" }
    )
    $runsColumns = @(
        @{ header = "Grupo"; key = "group"; type = "text" },
        @{ header = "Fase"; key = "phase"; type = "text" },
        @{ header = "Instancia"; key = "instance"; type = "text" },
        @{ header = "Alpha"; key = "alpha"; type = "number3" },
        @{ header = "Tenure"; key = "tenure"; type = "int" },
        @{ header = "Run"; key = "run"; type = "int" },
        @{ header = "Seed"; key = "seed"; type = "int" },
        @{ header = "OF"; key = "of"; type = "number2" },
        @{ header = "Tiempo (s)"; key = "elapsed_s"; type = "number3" }
    )
    @(
        (New-Sheet -Name "Resumen" -Rows $summaryRows),
        (New-Sheet -Name "Resumen configuraciones" -Rows (Build-TableRows -Objects $TsSummary -Columns $summaryColumns -HighlightBlock { param($row) $key = "{0}|{1}" -f $row.group, $row.phase; [double]::Parse($row.avg_dev_pct, $InvariantCulture) -eq $bestByGroupPhase[$key] }) -FreezeCell "A2" -AutoFilter $true),
        (New-Sheet -Name "Detalle instancias" -Rows (Build-TableRows -Objects $TsDetail -Columns $detailColumns) -FreezeCell "A2" -AutoFilter $true),
        (New-Sheet -Name "Runs" -Rows (Build-TableRows -Objects $TsRuns -Columns $runsColumns) -FreezeCell "A2" -AutoFilter $true),
        (Build-SourcesSheet -SourcePaths @(
            @{ role = "JSON resumen"; path = $CalibrationSummaryPath },
            @{ role = "CSV detalle"; path = $TsDetailPath },
            @{ role = "CSV resumen"; path = $TsSummaryPath },
            @{ role = "CSV runs"; path = $TsRunsPath }
        ))
    )
}

function Build-ComparisonWorkbookSheets {
    param([array]$ComparisonResults, [array]$ComparisonRuns, [pscustomobject]$ComparisonTests, [pscustomobject]$CalibrationSummary)
    $summaryRows = [System.Collections.Generic.List[object]]::new()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Comparacion final" -Style 1))
    Add-Row -Rows $summaryRows -Cells @()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Metadato" -Style 2), (New-TextCell -Value "Valor" -Style 2))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Instancias comparadas" -Style 3), (New-FormulaCell -Formula ("COUNTA('Comparacion instancias'!A2:A{0})" -f ($ComparisonResults.Count + 1)) -Style 8 -Display $ComparisonResults.Count.ToString($InvariantCulture)))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Instancias small" -Style 3), (New-FormulaCell -Formula ("COUNTIF('Comparacion instancias'!B2:B{0},""small"")" -f ($ComparisonResults.Count + 1)) -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Instancias large" -Style 3), (New-FormulaCell -Formula ("COUNTIF('Comparacion instancias'!B2:B{0},""large"")" -f ($ComparisonResults.Count + 1)) -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Runs por instancia" -Style 3), (New-IntegerCell -Value 5 -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Time limit por algoritmo (s)" -Style 3), (New-IntegerCell -Value 30 -Style 8))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Avg dev% GRASP (global)" -Style 3), (New-FormulaCell -Formula ("AVERAGE('Comparacion instancias'!I2:I{0})" -f ($ComparisonResults.Count + 1)) -Style 7))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Avg dev% TS (global)" -Style 3), (New-FormulaCell -Formula ("AVERAGE('Comparacion instancias'!R2:R{0})" -f ($ComparisonResults.Count + 1)) -Style 7))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Delta medio TS - GRASP" -Style 3), (New-FormulaCell -Formula ("AVERAGE('Comparacion instancias'!U2:U{0})" -f ($ComparisonResults.Count + 1)) -Style 5))
    Add-Row -Rows $summaryRows -Cells @()
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Wilcoxon por grupo" -Style 1))
    Add-Row -Rows $summaryRows -Cells @((New-TextCell -Value "Grupo" -Style 2), (New-TextCell -Value "Wins GRASP" -Style 2), (New-TextCell -Value "Wins TS" -Style 2), (New-TextCell -Value "Empates" -Style 2), (New-TextCell -Value "Mean delta (TS-GRASP)" -Style 2), (New-TextCell -Value "p-value" -Style 2), (New-TextCell -Value "Estado" -Style 2))
    foreach ($groupName in @("overall", "small", "large")) {
        $row = $ComparisonTests.$groupName
        $pValueCell = if ($row.status -eq "ok") { New-NumberCell -Value $row.pvalue -Style $(if ([double]$row.pvalue -lt 0.05) { 15 } else { 14 }) } else { New-TextCell -Value "-" -Style 4 }
        Add-Row -Rows $summaryRows -Cells @(
            (New-TextCell -Value $groupName -Style 4),
            (New-IntegerCell -Value $row.wins_grasp -Style 8),
            (New-IntegerCell -Value $row.wins_ts -Style 8),
            (New-IntegerCell -Value $row.ties -Style 8),
            (New-NumberCell -Value $row.mean_delta_ts_minus_grasp -Style 5),
            $pValueCell,
            (New-TextCell -Value $row.status -Style 4)
        )
    }
    $comparisonRows = [System.Collections.Generic.List[object]]::new()
    Add-Row -Rows $comparisonRows -Cells @(
        (New-TextCell -Value "Instancia" -Style 2), (New-TextCell -Value "Grupo" -Style 2), (New-TextCell -Value "Best known" -Style 2),
        (New-TextCell -Value "GRASP alpha" -Style 2), (New-TextCell -Value "GRASP avg OF" -Style 2), (New-TextCell -Value "GRASP best" -Style 2),
        (New-TextCell -Value "GRASP worst" -Style 2), (New-TextCell -Value "GRASP std" -Style 2), (New-TextCell -Value "GRASP dev%" -Style 2),
        (New-TextCell -Value "GRASP #best" -Style 2), (New-TextCell -Value "GRASP avg time" -Style 2), (New-TextCell -Value "TS alpha" -Style 2),
        (New-TextCell -Value "TS tenure" -Style 2), (New-TextCell -Value "TS avg OF" -Style 2), (New-TextCell -Value "TS best" -Style 2),
        (New-TextCell -Value "TS worst" -Style 2), (New-TextCell -Value "TS std" -Style 2), (New-TextCell -Value "TS dev%" -Style 2),
        (New-TextCell -Value "TS #best" -Style 2), (New-TextCell -Value "TS avg time" -Style 2), (New-TextCell -Value "Delta avg TS-GRASP" -Style 2),
        (New-TextCell -Value "Ganador promedio" -Style 2)
    )
    for ($i = 0; $i -lt $ComparisonResults.Count; $i++) {
        $row = $ComparisonResults[$i]
        $excelRow = $i + 2
        $delta = [double]::Parse($row.ts_avg_of, $InvariantCulture) - [double]::Parse($row.grasp_avg_of, $InvariantCulture)
        $highlight = $delta -gt 0
        $winner = if ($delta -gt 0) { "GRASP+TS" } elseif ($delta -lt 0) { "GRASP" } else { "Empate" }
        Add-Row -Rows $comparisonRows -Cells @(
            (New-CellFromValue -Value $row.instance -Type "text" -Highlight $highlight),
            (New-CellFromValue -Value $row.group -Type "text" -Highlight $highlight),
            (New-CellFromValue -Value $row.best_known -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_alpha -Type "number3" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_avg_of -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_best -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_worst -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_std -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_dev_pct -Type "percent" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_nbest -Type "int" -Highlight $highlight),
            (New-CellFromValue -Value $row.grasp_avg_time -Type "number3" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_alpha -Type "number3" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_tenure -Type "int" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_avg_of -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_best -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_worst -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_std -Type "number2" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_dev_pct -Type "percent" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_nbest -Type "int" -Highlight $highlight),
            (New-CellFromValue -Value $row.ts_avg_time -Type "number3" -Highlight $highlight),
            (New-FormulaCell -Formula ("N{0}-E{0}" -f $excelRow) -Style $(if ($highlight) { 10 } else { 5 }) -Display ([math]::Round($delta, 2).ToString($InvariantCulture))),
            (New-CellFromValue -Value $winner -Type "text" -Highlight $highlight)
        )
    }
    $runsColumns = @(
        @{ header = "Instancia"; key = "instance"; type = "text" },
        @{ header = "Grupo"; key = "group"; type = "text" },
        @{ header = "Algoritmo"; key = "algorithm"; type = "text" },
        @{ header = "Run"; key = "run"; type = "int" },
        @{ header = "Seed"; key = "seed"; type = "int" },
        @{ header = "Alpha"; key = "alpha"; type = "number3" },
        @{ header = "Tabu tenure"; expr = { param($row) if ([string]::IsNullOrWhiteSpace([string]$row.tabu_tenure)) { "-" } else { [string]$row.tabu_tenure } }; type = "text" },
        @{ header = "OF"; key = "of"; type = "number2" },
        @{ header = "Tiempo (s)"; key = "elapsed_s"; type = "number3" }
    )
    $testsRows = [System.Collections.Generic.List[object]]::new()
    Add-Row -Rows $testsRows -Cells @((New-TextCell -Value "Grupo" -Style 2), (New-TextCell -Value "N pares" -Style 2), (New-TextCell -Value "Wins GRASP" -Style 2), (New-TextCell -Value "Wins TS" -Style 2), (New-TextCell -Value "Empates" -Style 2), (New-TextCell -Value "Mean delta (TS-GRASP)" -Style 2), (New-TextCell -Value "Pares no cero" -Style 2), (New-TextCell -Value "Statistic" -Style 2), (New-TextCell -Value "p-value" -Style 2), (New-TextCell -Value "Estado" -Style 2))
    foreach ($groupName in @("overall", "small", "large")) {
        $row = $ComparisonTests.$groupName
        $pCell = if ($row.status -eq "ok") { New-NumberCell -Value $row.pvalue -Style $(if ([double]$row.pvalue -lt 0.05) { 15 } else { 14 }) } else { New-TextCell -Value "-" -Style 4 }
        $statCell = if ($row.status -eq "ok") { New-NumberCell -Value $row.statistic -Style 5 } else { New-TextCell -Value "-" -Style 4 }
        Add-Row -Rows $testsRows -Cells @(
            (New-TextCell -Value $groupName -Style 4),
            (New-IntegerCell -Value $row.n_pairs -Style 8),
            (New-IntegerCell -Value $row.wins_grasp -Style 8),
            (New-IntegerCell -Value $row.wins_ts -Style 8),
            (New-IntegerCell -Value $row.ties -Style 8),
            (New-NumberCell -Value $row.mean_delta_ts_minus_grasp -Style 5),
            (New-TextCell -Value $(if ($row.PSObject.Properties.Match("non_zero_pairs").Count -gt 0) { [string]$row.non_zero_pairs } else { "-" }) -Style 4),
            $statCell,
            $pCell,
            (New-TextCell -Value $(if ($row.status -eq "ok") { $row.status } else { "{0}: {1}" -f $row.status, $row.reason }) -Style 4)
        )
    }
    $paramsRows = [System.Collections.Generic.List[object]]::new()
    Add-Row -Rows $paramsRows -Cells @((New-TextCell -Value "Grupo" -Style 2), (New-TextCell -Value "Etiqueta" -Style 2), (New-TextCell -Value "GRASP alpha" -Style 2), (New-TextCell -Value "GRASP best avg dev%" -Style 2), (New-TextCell -Value "TS alpha" -Style 2), (New-TextCell -Value "TS tenure" -Style 2), (New-TextCell -Value "TS best avg dev%" -Style 2))
    foreach ($groupName in @("small", "large")) {
        $group = $CalibrationSummary.groups.$groupName
        Add-Row -Rows $paramsRows -Cells @(
            (New-TextCell -Value $groupName -Style 4),
            (New-TextCell -Value $group.label -Style 4),
            (New-NumberCell -Value $group.grasp.best_alpha -Style 6),
            (New-NumberCell -Value $group.grasp.best_avg_dev_pct -Style 7),
            (New-NumberCell -Value $group.ts.best_alpha -Style 6),
            (New-IntegerCell -Value $group.ts.best_tenure -Style 8),
            (New-NumberCell -Value $group.ts.best_avg_dev_pct -Style 7)
        )
    }
    @(
        (New-Sheet -Name "Resumen" -Rows $summaryRows),
        (New-Sheet -Name "Comparacion instancias" -Rows $comparisonRows -FreezeCell "A2" -AutoFilter $true),
        (New-Sheet -Name "Runs pareados" -Rows (Build-TableRows -Objects $ComparisonRuns -Columns $runsColumns) -FreezeCell "A2" -AutoFilter $true),
        (New-Sheet -Name "Test estadistico" -Rows $testsRows -FreezeCell "A2" -AutoFilter $true),
        (New-Sheet -Name "Parametros calibrados" -Rows $paramsRows -FreezeCell "A2" -AutoFilter $true),
        (Build-SourcesSheet -SourcePaths @(
            @{ role = "JSON calibracion"; path = $CalibrationSummaryPath },
            @{ role = "CSV resultados"; path = $ComparisonResultsPath },
            @{ role = "CSV runs"; path = $ComparisonRunsPath },
            @{ role = "JSON tests"; path = $ComparisonTestsPath }
        ))
    )
}

function Convert-CellForCombinedSheet {
    param([object]$Cell)
    if ($Cell.kind -ne "formula") {
        return $Cell
    }
    if ([string]::IsNullOrWhiteSpace([string]$Cell.display)) {
        return New-TextCell -Value "" -Style 4
    }
    try {
        $number = [double]::Parse([string]$Cell.display, $InvariantCulture)
        return [pscustomobject]@{
            kind    = "number"
            value   = $number.ToString($InvariantCulture)
            style   = $Cell.style
            display = [string]$Cell.display
        }
    }
    catch {
        return New-TextCell -Value $Cell.display -Style 4
    }
}

function Build-CombinedSheet {
    param([string]$SheetName, [array]$Blocks)
    $rows = [System.Collections.Generic.List[object]]::new()
    Add-Row -Rows $rows -Cells @((New-TextCell -Value $SheetName -Style 1))
    Add-Row -Rows $rows -Cells @()
    $firstBlock = $true
    foreach ($block in $Blocks) {
        if (-not $firstBlock) {
            Add-Row -Rows $rows -Cells @()
            Add-Row -Rows $rows -Cells @()
        }
        Add-Row -Rows $rows -Cells @((New-TextCell -Value $block.Name -Style 1))
        Add-Row -Rows $rows -Cells @()
        foreach ($sourceRow in $block.Rows) {
            $convertedCells = [System.Collections.Generic.List[object]]::new()
            foreach ($cell in $sourceRow) {
                $convertedCells.Add((Convert-CellForCombinedSheet -Cell $cell)) | Out-Null
            }
            Add-Row -Rows $rows -Cells $convertedCells.ToArray()
        }
        $firstBlock = $false
    }
    New-Sheet -Name $SheetName -Rows $rows
}

function Build-UnifiedWorkbookSheets {
    param([array]$GraspSheets, [array]$TsSheets, [array]$ComparisonSheets)
    @(
        (Build-CombinedSheet -SheetName "Calibracion GRASP" -Blocks $GraspSheets),
        (Build-CombinedSheet -SheetName "Calibracion TS" -Blocks $TsSheets),
        (Build-CombinedSheet -SheetName "Comparacion final" -Blocks $ComparisonSheets)
    )
}

Ensure-Directory $OutputDir
Ensure-Directory $TempRoot

$calibrationSummary = Get-Content -LiteralPath $CalibrationSummaryPath -Raw | ConvertFrom-Json
$graspDetail = Import-Csv -LiteralPath $GraspDetailPath
$graspSummary = Import-Csv -LiteralPath $GraspSummaryPath
$graspRuns = Import-Csv -LiteralPath $GraspRunsPath
$tsDetail = Import-Csv -LiteralPath $TsDetailPath
$tsSummary = Import-Csv -LiteralPath $TsSummaryPath
$tsRuns = Import-Csv -LiteralPath $TsRunsPath
$comparisonResults = Import-Csv -LiteralPath $ComparisonResultsPath
$comparisonRuns = Import-Csv -LiteralPath $ComparisonRunsPath
$comparisonTests = Get-Content -LiteralPath $ComparisonTestsPath -Raw | ConvertFrom-Json

$graspSheets = Build-GraspWorkbookSheets -GraspDetail $graspDetail -GraspSummary $graspSummary -GraspRuns $graspRuns -CalibrationSummary $calibrationSummary
$tsSheets = Build-TsWorkbookSheets -TsDetail $tsDetail -TsSummary $tsSummary -TsRuns $tsRuns -CalibrationSummary $calibrationSummary
$comparisonSheets = Build-ComparisonWorkbookSheets -ComparisonResults $comparisonResults -ComparisonRuns $comparisonRuns -ComparisonTests $comparisonTests -CalibrationSummary $calibrationSummary
$unifiedSheets = Build-UnifiedWorkbookSheets -GraspSheets $graspSheets -TsSheets $tsSheets -ComparisonSheets $comparisonSheets

Write-XlsxWorkbook -OutputPath $GraspWorkbookPath -Title "Calibracion GRASP" -Sheets $graspSheets
Write-XlsxWorkbook -OutputPath $TsWorkbookPath -Title "Calibracion TS" -Sheets $tsSheets
Write-XlsxWorkbook -OutputPath $ComparisonWorkbookPath -Title "Comparacion final" -Sheets $comparisonSheets
Write-XlsxWorkbook -OutputPath $UnifiedWorkbookPath -Title "Experimentacion completa" -Sheets $unifiedSheets

Write-Output "Generated workbooks:"
Write-Output ("- " + (Get-FullPath $GraspWorkbookPath))
Write-Output ("- " + (Get-FullPath $TsWorkbookPath))
Write-Output ("- " + (Get-FullPath $ComparisonWorkbookPath))
Write-Output ("- " + (Get-FullPath $UnifiedWorkbookPath))
