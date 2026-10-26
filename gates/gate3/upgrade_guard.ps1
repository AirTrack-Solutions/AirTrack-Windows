# Windows installer transaction guard. Requires explicit administrator approval.
[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][ValidateSet('Prepare','Finish','Rollback')][string]$Mode,
 [Parameter(Mandatory=$true)][string]$InstallDir,
 [ValidatePattern('^[A-Za-z][A-Za-z0-9_-]{1,63}$')][string]$ServiceName='AirTrackClient',
 [string]$ExpectedVersion='1.0.1',
 [Parameter(Mandatory=$true)][string]$StateFile
)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
$principal=New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if(-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){throw 'Administrator approval is required'}
function Ini([string]$File){
 $result=@{};$section=''
 foreach($line in [IO.File]::ReadAllLines($File)){
  $s=$line.Trim();if(-not $s -or $s.StartsWith('#') -or $s.StartsWith(';')){continue}
  if($s -match '^\[([^\]]+)\]$'){$section=$matches[1];$result[$section]=@{};continue}
  if($s.Contains('=') -and $section){$parts=$s.Split(@('='),2);$result[$section][$parts[0].Trim()]=$parts[1].Trim()}
 };return $result
}
function NoLinks([string]$Path){
 if((Get-Item -LiteralPath $Path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked installation paths are not supported'}
 if(@(Get-ChildItem -LiteralPath $Path -Force -Recurse | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){throw 'Linked files/directories require manual review before updating'}
}
function CopyTree([string]$Source,[string]$Destination){
 New-Item -ItemType Directory -Path $Destination -Force | Out-Null
 & robocopy.exe $Source $Destination /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ /NFL /NDL /NJH /NJS /NP | Out-Null
 if($LASTEXITCODE -gt 7){throw 'Application snapshot/copy failed'}
}
function ServiceExe([string]$Name){
 $s=Get-CimInstance Win32_Service -Filter "Name='$Name'"
 if(-not $s){throw 'Existing application service was not found'}
 if($s.PathName -notmatch '^\s*"([^"]+)"') {throw 'Service executable path must be quoted'}
 return [IO.Path]::GetFullPath($matches[1])
}
function SaveState($State){
 $tmp=$StateFile+'.new';[IO.File]::WriteAllText($tmp,($State|ConvertTo-Json -Depth 6),(New-Object Text.UTF8Encoding($false)));Move-Item -LiteralPath $tmp -Destination $StateFile -Force
}
function StopApp(){
 $s=Get-Service -Name $ServiceName
 if($s.Status -ne 'Stopped'){Stop-Service -Name $ServiceName; (Get-Service $ServiceName).WaitForStatus('Stopped',[TimeSpan]::FromSeconds(45))}
}
function StartApp(){
 if((Get-Service $ServiceName).Status -ne 'Running'){Start-Service $ServiceName;(Get-Service $ServiceName).WaitForStatus('Running',[TimeSpan]::FromSeconds(45))}
}
function Options($Config,[string]$Path){
 $hostName=$Config.database.host;if(-not $hostName){$hostName='127.0.0.1'}
 if($hostName -notin @('127.0.0.1','localhost')){throw 'This upgrade flow requires a local application database'}
 $port=$Config.database.port;if(-not $port){$port='3307'}
 if($port -notmatch '^\d{1,5}$' -or [int]$port -lt 1 -or [int]$port -gt 65535){throw 'Invalid local database port'}
 $user=$Config.database.user;$password=$Config.database.password
 if(-not $user -or $user.Contains("`n") -or $password.Contains("`n") -or $password.Contains("`r")){throw 'Unsupported database configuration'}
 $escape={$args[0].Replace('\','\\').Replace('"','\"')}
 $text="[client]`r`nhost=$hostName`r`nport=$port`r`nuser=`"$(& $escape $user)`"`r`npassword=`"$(& $escape $password)`"`r`n"
 [IO.File]::WriteAllText($Path,$text,(New-Object Text.UTF8Encoding($false)))
}
function Native([string]$File,[string[]]$Arguments,[string]$ErrorLog,[string]$InputFile=''){
 $params=@{FilePath=$File;ArgumentList=$Arguments;PassThru=$true;NoNewWindow=$true;RedirectStandardError=$ErrorLog;RedirectStandardOutput=($ErrorLog+'.out')}
 if($InputFile){$params.RedirectStandardInput=$InputFile}
 $p=Start-Process @params
 if(-not $p.WaitForExit(120000)){ $p.Kill();$p.WaitForExit();throw 'Database operation timed out'}
 # Refresh is needed for reliable ExitCode after redirected Start-Process.
 $p.Refresh();if($p.ExitCode -ne 0){throw 'Database backup/restore failed; see protected recovery log'}
}
function RestoreState($State){
 StopApp
 $config=Ini (Join-Path $State.backup 'application\airtrack.cfg')
 $option=Join-Path $State.backup 'recovery-client.ini'
 try{
  Options $config $option
  Native (Join-Path $State.db_bin 'mariadb.exe') @("--defaults-extra-file=`"$option`"") (Join-Path $State.backup 'restore-error.log') (Join-Path $State.backup 'database.sql')
 }finally{Remove-Item -LiteralPath $option -ErrorAction SilentlyContinue}
 # Target was verified as the service's application directory. Restore the
 # entire snapshot, rather than overlaying new/obsolete code together.
 NoLinks $InstallDir
 Get-ChildItem -LiteralPath $InstallDir -Force | Remove-Item -Recurse -Force
 CopyTree (Join-Path $State.backup 'application') $InstallDir
 Remove-Item -LiteralPath $State.flag -ErrorAction SilentlyContinue
 StartApp
 $State.phase='rolled_back';SaveState $State
}
$InstallDir=[IO.Path]::GetFullPath($InstallDir).TrimEnd('\')
if(-not (Test-Path -LiteralPath (Join-Path $InstallDir 'airtrack.cfg'))){throw 'Existing configuration missing; refusing an upgrade'}
if((ServiceExe $ServiceName) -ine (Join-Path $InstallDir 'AirTrack.exe')){throw 'Installer target does not match the registered service'}
NoLinks $InstallDir
if($Mode -eq 'Prepare'){
 if(Test-Path -LiteralPath $StateFile){$old=Get-Content -LiteralPath $StateFile -Raw|ConvertFrom-Json;if($old.phase -notin @('completed','rolled_back')){throw 'An earlier update requires recovery before another update'}}
 $config=Ini (Join-Path $InstallDir 'airtrack.cfg')
 $installedMeta=Join-Path $InstallDir '_internal\app\windows_release.json'
 if(Test-Path $installedMeta){$installed=Get-Content $installedMeta -Raw|ConvertFrom-Json;if([version]$installed.version -gt [version]$ExpectedVersion){throw 'Refusing to replace a newer application version'}}
 $environment=(Get-ItemProperty ('HKLM:\SYSTEM\CurrentControlSet\Services\'+$ServiceName) -Name Environment -ErrorAction SilentlyContinue).Environment
 if(@($environment | Where-Object {$_ -match '^(DATABASE_URI|DB_HOST|DB_PORT|DB_NAME|DB_USER|DB_PASSWORD|AIRTRACK_HOME|AIRTRACK_PORT)='}).Count){throw 'Service environment overrides require manual review before updating'}
 if($config.database.uri){
  $uri=[uri]$config.database.uri;$credentials=$uri.UserInfo.Split(@(':'),2)
  if($uri.Host -ine $config.database.host -or $uri.Port -ne [int]$config.database.port -or [uri]::UnescapeDataString($uri.AbsolutePath.Trim('/')) -ne $config.database.name -or [uri]::UnescapeDataString($credentials[0]) -ne $config.database.user -or $credentials.Count -ne 2 -or [uri]::UnescapeDataString($credentials[1]) -cne $config.database.password){throw 'Database URI differs from backup connection fields; refusing an unsafe backup'}
 }
 $home=$config.app.data_dir;if(-not $home){$home=Join-Path $env:ProgramData 'AirTrack'}
 $home=[IO.Path]::GetFullPath($home).TrimEnd('\')
 if($home.StartsWith($InstallDir+'\',[StringComparison]::OrdinalIgnoreCase) -or $home -ieq $InstallDir){throw 'Move application data outside the program folder before using this upgrade flow'}
 if($config.database.name -notmatch '^[A-Za-z0-9_]+$'){throw 'Unsupported database name'}
 $updates=Join-Path $home 'updates';New-Item -ItemType Directory -Path $updates -Force|Out-Null
 & icacls.exe $updates /inheritance:r /grant:r '*S-1-5-32-544:(OI)(CI)F' '*S-1-5-18:(OI)(CI)F' | Out-Null
 if($LASTEXITCODE -ne 0){throw 'Cannot secure update backups'}
 if([IO.Path]::GetDirectoryName([IO.Path]::GetFullPath($StateFile)) -ine $updates){throw 'Unexpected transaction state directory'}
 $backup=Join-Path $updates ('backups\'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory -Path $backup -Force|Out-Null
 $db=Get-CimInstance Win32_Service -Filter "Name='AirTrackDB'";if(-not $db -or $db.PathName -notmatch '^\s*"([^"]+)"'){throw 'Cannot locate the installed database tools'}
 $dbBin=Split-Path $matches[1];if(-not(Test-Path (Join-Path $dbBin 'mariadb-dump.exe'))){throw 'Database backup tool unavailable'}
 $port=$config.app.port;if(-not $port){$port=5000};if([int]$port -lt 1 -or [int]$port -gt 65535){throw 'Invalid application port'}
 $state=[ordered]@{phase='preparing';install_dir=$InstallDir;service=$ServiceName;backup=$backup;flag=(Join-Path $home 'update-in-progress.json');db_bin=$dbBin;db_name=$config.database.name;port=[int]$port;version=$ExpectedVersion}
 Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $backup 'recover.ps1');SaveState $state
 try{
  StopApp
  [IO.File]::WriteAllText($state.flag,($state|ConvertTo-Json))
  CopyTree $InstallDir (Join-Path $backup 'application')
  $option=Join-Path $backup 'backup-client.ini'
  try{
   Options $config $option
   Native (Join-Path $dbBin 'mariadb-dump.exe') @("--defaults-extra-file=`"$option`"",'--single-transaction','--skip-lock-tables','--no-tablespaces','--databases','--add-drop-database',"--result-file=`"$(Join-Path $backup 'database.sql')`"",$config.database.name) (Join-Path $backup 'backup-error.log')
   if((Get-Item (Join-Path $backup 'database.sql')).Length -lt 128){throw 'Database backup is incomplete'}
  }finally{Remove-Item -LiteralPath $option -ErrorAction SilentlyContinue}
  $state.phase='prepared';SaveState $state
 }catch{
  Remove-Item -LiteralPath $state.flag -ErrorAction SilentlyContinue
  StartApp;$state.phase='rolled_back';SaveState $state;throw
 }
}elseif($Mode -in @('Finish','Rollback')){
 $state=Get-Content -LiteralPath $StateFile -Raw|ConvertFrom-Json
 if($Mode -eq 'Rollback' -and $state.phase -eq 'rolled_back' -and $state.install_dir -ieq $InstallDir -and $state.service -eq $ServiceName){exit 0}
 if($Mode -eq 'Rollback' -and $state.phase -eq 'preparing' -and $state.install_dir -ieq $InstallDir -and $state.service -eq $ServiceName){
  Remove-Item -LiteralPath $state.flag -ErrorAction SilentlyContinue;StartApp;$state.phase='rolled_back';SaveState $state;exit 0
 }
 if($state.install_dir -ine $InstallDir -or $state.service -ne $ServiceName -or $state.phase -notin @('prepared','checking')){throw 'Invalid or already completed recovery state'}
 $expectedRoot=Join-Path (Split-Path $StateFile) 'backups'
 if(-not ([IO.Path]::GetFullPath($state.backup)).StartsWith($expectedRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Invalid backup path'}
 if($Mode -eq 'Rollback'){RestoreState $state;exit 0}
 try{
  # Restore writable data embedded in old installations, not obsolete code.
  foreach($rel in @('airtrack.cfg','license.lic','logs','pics','backups','export','data','_internal\app\static\uploads','_internal\app\pics','_internal\app\backups','_internal\app\export','_internal\app\runtime','_internal\app\data','_internal\app\config.json','_internal\config\license.lic','_internal\app\config\license.lic')){
   $source=Join-Path (Join-Path $state.backup 'application') $rel;$dest=Join-Path $InstallDir $rel
   if(Test-Path -LiteralPath $source){New-Item -ItemType Directory -Path (Split-Path $dest) -Force|Out-Null;if((Get-Item $source).PSIsContainer){CopyTree $source $dest}else{Copy-Item -LiteralPath $source -Destination $dest -Force}}
  }
  $license=Join-Path (Split-Path $state.flag) 'license.lic';if(Test-Path $license){$dest=Join-Path $InstallDir '_internal\config\license.lic';New-Item -ItemType Directory -Path (Split-Path $dest) -Force|Out-Null;Copy-Item $license $dest -Force}
  $state.phase='checking';SaveState $state;StartApp
  $healthy=$false
  for($i=0;$i -lt 45;$i++){
   try{$r=Invoke-RestMethod -Uri "http://127.0.0.1:$($state.port)/updates/api/version" -TimeoutSec 2;if($r.product -eq 'AirTrack-Windows' -and $r.version -eq $state.version -and $r.database_ready){$healthy=$true;break}}catch{}
   Start-Sleep -Seconds 1
  }
  if(-not $healthy){throw 'Updated application failed its version/database health check'}
  Remove-Item -LiteralPath $state.flag -ErrorAction Stop
  $state.phase='completed';SaveState $state
 }catch{
  $failure=$_;RestoreState $state;throw ('Update failed and was restored: '+$failure.Exception.Message)
 }
}
