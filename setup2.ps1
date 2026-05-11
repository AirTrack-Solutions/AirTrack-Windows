# AirTrack Windows — Diagnostic Installer
# Run this if the standard installer fails.
# It will show detailed error information you can send to support.

$ErrorActionPreference = 'Stop'
$url = 'https://raw.githubusercontent.com/Subhuti/AirTrack-Windows/main/setup-airtrack.ps1'
try {
    Write-Host "Fetching $url ..."
    $script = Invoke-RestMethod -Uri $url
    Write-Host ("Downloaded {0} bytes. Executing..." -f $script.Length)
    Write-Host ""
    Invoke-Expression $script
}
catch {
    $err = $_
    Write-Host ""
    Write-Host "==================== ERROR ====================" -ForegroundColor Red
    Write-Host ("Type   : {0}" -f $err.Exception.GetType().FullName) -ForegroundColor Yellow
    Write-Host ("Message: {0}" -f $err.Exception.Message) -ForegroundColor Yellow
    if ($err.InvocationInfo) {
        Write-Host ""
        Write-Host "Location:" -ForegroundColor Yellow
        Write-Host ("  Line   : {0}" -f $err.InvocationInfo.ScriptLineNumber)
        Write-Host ("  Column : {0}" -f $err.InvocationInfo.OffsetInLine)
        if ($err.InvocationInfo.Line) {
            Write-Host ("  Source : {0}" -f $err.InvocationInfo.Line.TrimEnd())
        }
    }
    if ($err.Exception.InnerException) {
        Write-Host ""
        Write-Host "Inner exception:" -ForegroundColor Yellow
        Write-Host ("  {0}: {1}" -f `
            $err.Exception.InnerException.GetType().FullName, `
            $err.Exception.InnerException.Message)
    }
    Write-Host ""
    Write-Host "Script stack trace:" -ForegroundColor Yellow
    Write-Host $err.ScriptStackTrace
    Write-Host ""
    Write-Host "Full error record:" -ForegroundColor Yellow
    Write-Host ($err | Format-List * -Force | Out-String)
    Write-Host "===============================================" -ForegroundColor Red
}
finally {
    Write-Host ""
    Write-Host "Press Enter to close..."
    [void][System.Console]::ReadLine()
}
