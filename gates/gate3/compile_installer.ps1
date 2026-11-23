$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$version = (Get-Content (Join-Path $repo 'app\windows_release.json') -Raw | ConvertFrom-Json).version
if ($version -notmatch '^\d+\.\d+\.\d+$') { throw 'Invalid installer release version' }
$compiler = Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe'
if (-not (Test-Path $compiler)) { throw 'Install Inno Setup 6 before compiling the installer' }
Copy-Item (Join-Path $repo 'app\db\schema.sql') (Join-Path $PSScriptRoot 'schema.sql') -Force
Push-Location $PSScriptRoot
try {
    & $compiler ("/DReleaseVersion=" + $version) 'setup.iss'
    if ($LASTEXITCODE -ne 0) { throw 'Installer compilation failed' }
} finally { Pop-Location }
