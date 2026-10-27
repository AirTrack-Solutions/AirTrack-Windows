[CmdletBinding()]
param(
 [ValidateSet('Register','Run')][string]$Mode='Run',
 [Parameter(Mandatory=$true)][string]$InstallDir,
 [Parameter(Mandatory=$true)][string]$DataDir,
 [ValidatePattern('^[A-Za-z][A-Za-z0-9_-]{1,63}$')][string]$ServiceName='AirTrackClient'
)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$updates=Join-Path $DataDir 'updates'
$taskName='AirTrack-Update-'+$ServiceName
$runner=Join-Path $updates 'automatic_updates.ps1'
if($Mode -eq 'Register'){
 New-Item -ItemType Directory -Path $updates -Force|Out-Null
 & icacls.exe $updates /inheritance:r /grant:r '*S-1-5-32-544:(OI)(CI)F' '*S-1-5-18:(OI)(CI)F'|Out-Null
 if($LASTEXITCODE -ne 0){throw 'Cannot protect automatic updater'}
 Copy-Item -LiteralPath $PSCommandPath -Destination $runner -Force
 $arguments='-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "'+$runner+'" -Mode Run -InstallDir "'+$InstallDir+'" -DataDir "'+$DataDir+'" -ServiceName "'+$ServiceName+'"'
 $action=New-ScheduledTaskAction -Execute ($env:SystemRoot+'\System32\WindowsPowerShell\v1.0\powershell.exe') -Argument $arguments
 $trigger=New-ScheduledTaskTrigger -Daily -At '03:00'
 $settings=New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 2) -RunOnlyIfIdle -IdleDuration (New-TimeSpan -Minutes 10) -IdleWaitTimeout (New-TimeSpan -Hours 1) -DontStopOnIdleEnd
 Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -User 'SYSTEM' -RunLevel Highest -Force|Out-Null
 exit 0
}
$stateFile=Join-Path $updates ('active-'+$ServiceName+'.json')
if(Test-Path $stateFile){
 $state=Get-Content -LiteralPath $stateFile -Raw|ConvertFrom-Json
 if($state.phase -notin @('completed','rolled_back')){
  $recovery=Join-Path $state.backup 'recover.ps1'
  $backupRoot=[IO.Path]::GetFullPath((Join-Path $updates 'backups'))+'\'
  if(-not ([IO.Path]::GetFullPath($state.backup)).StartsWith($backupRoot,[StringComparison]::OrdinalIgnoreCase)){throw 'Unexpected recovery directory'}
  & powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File $recovery -Mode Rollback -InstallDir $InstallDir -ServiceName $ServiceName -StateFile $stateFile
  if($LASTEXITCODE -ne 0){throw 'Interrupted update requires recovery; no new installer will run'}
  # Recovery is the only action in this run; avoid immediately retrying
  # the same release after an interrupted or failed update.
  exit 0
 }
}
$exe=Join-Path $InstallDir 'AirTrack.exe'
$output=& $exe stage-update
if($LASTEXITCODE -ne 0){exit 1}
$result=($output -join "`n")|ConvertFrom-Json
if($result.status -ne 'ready'){exit 0}
$installer=[IO.Path]::GetFullPath($result.installer)
$downloadRoot=[IO.Path]::GetFullPath((Join-Path $updates 'downloads'))+'\'
if(-not $installer.StartsWith($downloadRoot,[StringComparison]::OrdinalIgnoreCase)){throw 'Unexpected installer directory'}
if((Get-Item -LiteralPath $installer).Length -ne $result.size -or (Get-FileHash -LiteralPath $installer -Algorithm SHA256).Hash.ToLowerInvariant() -cne $result.sha256){throw 'Staged installer changed; refusing execution'}
$log=Join-Path $updates ('install-'+$result.version+'.log')
$process=Start-Process -FilePath $installer -ArgumentList @('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART',('/SERVICENAME='+$ServiceName),('/LOG="'+$log+'"')) -PassThru
$handle=$process.Handle
if(-not $process.WaitForExit(3600000)){throw 'Installer is still running; inspect transaction state'}
if($process.ExitCode -ne 0){
 $result|ConvertTo-Json|Set-Content (Join-Path $updates 'failed-release.json') -Encoding UTF8
 @{status='error';error='Automatic installation failed. Inspect the recovery state before retrying.';checked_at=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content (Join-Path $updates 'automatic-status.json') -Encoding UTF8
 throw 'Automatic installation failed; inspect protected update logs'
}
@{status='installed';version=$result.version;checked_at=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content (Join-Path $updates 'automatic-status.json') -Encoding UTF8
