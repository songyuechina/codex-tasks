param(
    [ValidateSet("both", "acad_aag", "acadauto")]
    [string]$Doc = "both",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$hh = Join-Path $env:WINDIR "hh.exe"

if (-not (Test-Path $hh)) {
    throw "hh.exe not found: $hh"
}

$targets = @()
if ($Doc -eq "both" -or $Doc -eq "acad_aag") {
    $targets += @{ Name = "acad_aag"; Chm = Join-Path $root "acad_aag.chm"; Out = Join-Path $root "01_extracted_html\acad_aag" }
}
if ($Doc -eq "both" -or $Doc -eq "acadauto") {
    $targets += @{ Name = "acadauto"; Chm = Join-Path $root "acadauto.chm"; Out = Join-Path $root "01_extracted_html\acadauto" }
}

foreach ($target in $targets) {
    if (-not (Test-Path $target.Chm)) {
        throw "Missing CHM: $($target.Chm)"
    }

    if ($Force -and (Test-Path $target.Out)) {
        Remove-Item -LiteralPath $target.Out -Recurse -Force
    }

    New-Item -ItemType Directory -Force $target.Out | Out-Null
    Write-Output "Extracting $($target.Name) -> $($target.Out)"
    & $hh -decompile $target.Out $target.Chm | Out-Null
    Start-Sleep -Seconds 2

    $count = (Get-ChildItem -Path $target.Out -Recurse -File -ErrorAction SilentlyContinue | Measure-Object).Count
    if ($count -le 0) {
        throw "No files extracted for $($target.Name)"
    }
    Write-Output "Extracted $count files for $($target.Name)"
}

Write-Output "CHM extraction completed."
