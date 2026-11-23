param(
 [Parameter(Mandatory=$true)][string]$InstallDir,
 [Parameter(Mandatory=$true)][string]$MsiPath,
 [Parameter(Mandatory=$true)][string]$SchemaPath,
 [Parameter(Mandatory=$true)][string]$ExpectedVersion,
 [string]$ServiceName='AirTrackClient'
)
$ErrorActionPreference='Stop'
function Native([string]$File,[string[]]$Arguments) {
 & $File @Arguments | Out-Null
 if($LASTEXITCODE -ne 0){throw ('Required install step failed: '+[IO.Path]::GetFileName($File)+' (exit '+$LASTEXITCODE+')')}
}
function Protect([string]$Path) {
 Native 'icacls.exe' @($Path,'/inheritance:r','/grant:r','*S-1-5-18:(OI)(CI)F','*S-1-5-32-544:(OI)(CI)F')
}
function ReadIni([string]$Path) {
 $result=@{};$section=''
 foreach($line in [IO.File]::ReadAllLines($Path)) {
  $s=$line.Trim();if($s -match '^\[([^\]]+)\]$'){$section=$Matches[1].ToLowerInvariant();$result[$section]=@{};continue}
  if($s -match '^([^=;#]+)=(.*)$' -and $section){$result[$section][$Matches[1].Trim().ToLowerInvariant()]=$Matches[2].Trim()}
 }
 return $result
}
$utf8=New-Object System.Text.UTF8Encoding($false)
$cfgPath=Join-Path $InstallDir 'airtrack.cfg'
$licPath=Join-Path $InstallDir '_internal\config\license.lic'
if(-not(Test-Path $cfgPath) -or -not(Test-Path $licPath)){throw 'Keep airtrack.cfg and license.lic beside the installer when installing'}
if($ServiceName -notmatch '^AirTrack[A-Za-z0-9_-]*$'){throw 'Invalid AirTrack service name'}
if(Get-Service -Name $ServiceName -ErrorAction SilentlyContinue){throw 'Application service already exists; use the upgrade flow'}
if(Get-Service -Name 'AirTrackDB' -ErrorAction SilentlyContinue){throw 'An AirTrack database already exists; recover or upgrade it instead of creating a fresh database'}
$config=ReadIni $cfgPath
$dbName=$config.database.name;$dbUser=$config.database.user;$dbPassword=$config.database.password
$dbPort=3307;if($config.database.port){$dbPort=[int]$config.database.port}
$appPort=5000;if($config.app.port){$appPort=[int]$config.app.port}
if($config.database.host -notin @('127.0.0.1','localhost')){throw 'Fresh installation requires a local database'}
if($dbName -notmatch '^[A-Za-z0-9_]+$' -or $dbUser -notmatch '^[A-Za-z0-9_]+$' -or $dbPassword -notmatch '^[A-Za-z0-9_!@#%+=.-]{16,128}$'){throw 'Invalid database settings in customer configuration'}
if($dbPort -lt 1024 -or $dbPort -gt 65535 -or $appPort -lt 1024 -or $appPort -gt 65535 -or $dbPort -eq $appPort){throw 'Invalid local service ports'}
foreach($port in @($dbPort,$appPort)){if(Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue){throw ('Local port '+$port+' is already in use')}}
$dataHome=$config.app.data_dir;if(-not $dataHome){$dataHome=Join-Path $env:ProgramData 'AirTrack'}
$dataHome=[IO.Path]::GetFullPath($dataHome);$data=Join-Path $dataHome 'database'
if((Test-Path $data) -and (Get-ChildItem -LiteralPath $data -Force | Select-Object -First 1)){throw 'Existing database files found; fresh install will not overwrite them'}
New-Item -ItemType Directory -Path $dataHome -Force|Out-Null
Protect $dataHome
$programFiles64=$env:ProgramW6432;if(-not $programFiles64){$programFiles64=$env:ProgramFiles}
$bin=Join-Path $programFiles64 'MariaDB 11.4\bin'
$random=New-Object byte[] 32;$rng=[Security.Cryptography.RandomNumberGenerator]::Create();$rng.GetBytes($random);$rng.Dispose()
$rootPassword=[Convert]::ToBase64String($random).TrimEnd('=').Replace('+','-').Replace('/','_')
$private=Join-Path $env:TEMP ('AirTrack-setup-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $private|Out-Null;Protect $private
try {
 if(-not(Test-Path (Join-Path $bin 'mariadb-install-db.exe'))) {
  if(-not(Test-Path $MsiPath)){throw 'Bundled MariaDB installer is missing'}
  $args=@('/i',('"'+$MsiPath+'"'),'/quiet','/norestart','SERVICENAME=AirTrackDB',('PORT='+$dbPort),('PASSWORD='+$rootPassword),'ALLOWREMOTEMACHINE=0','BUFFERPOOLSIZE=64',('DATADIR="'+$data+'"'))
  $p=Start-Process -FilePath 'msiexec.exe' -ArgumentList $args -Wait -PassThru
  if($p.ExitCode -notin @(0,3010)){throw ('MariaDB installation failed (exit '+$p.ExitCode+')')}
 } else {
  Native (Join-Path $bin 'mariadb-install-db.exe') @("--datadir=$data","--service=AirTrackDB","--password=$rootPassword","--port=$dbPort","--silent")
 }
 $ini=Join-Path $data 'my.ini'
 if(-not(Test-Path $ini)){throw 'MariaDB instance configuration was not created'}
 Stop-Service -Name AirTrackDB -ErrorAction SilentlyContinue
 $dbIni=[IO.File]::ReadAllText($ini)
 if($dbIni -match '(?m)^\s*bind-address\s*='){$dbIni=[regex]::Replace($dbIni,'(?m)^\s*bind-address\s*=.*$','bind-address=127.0.0.1')}
 else{$dbIni=[regex]::Replace($dbIni,'(?m)^\[mysqld\]\s*$','[mysqld]'+"`r`nbind-address=127.0.0.1")}
 [IO.File]::WriteAllText($ini,$dbIni,$utf8)
 Start-Service AirTrackDB
 $ready=$false
 for($i=0;$i -lt 60;$i++){
  try{$tcp=New-Object Net.Sockets.TcpClient('127.0.0.1',$dbPort);$tcp.Close();$ready=$true;break}catch{Start-Sleep -Seconds 1}
 }
 if(-not $ready){throw 'MariaDB did not start; see the database error log'}
 $options=Join-Path $private 'root-client.ini'
 [IO.File]::WriteAllText($options,"[client]`r`nuser=root`r`npassword=$rootPassword`r`nhost=127.0.0.1`r`nport=$dbPort`r`nprotocol=tcp`r`n",$utf8)
 $sql=Join-Path $private 'initialize.sql'
 $schema=[IO.File]::ReadAllText($SchemaPath)
 $bootstrap="CREATE DATABASE ``$dbName`` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`r`nCREATE USER '$dbUser'@'127.0.0.1' IDENTIFIED BY '$dbPassword';`r`nGRANT ALL PRIVILEGES ON ``$dbName``.* TO '$dbUser'@'127.0.0.1';`r`nUSE ``$dbName``;`r`n"
 [IO.File]::WriteAllText($sql,$bootstrap+$schema,$utf8)
 # Source paths use forward slashes for MariaDB's client command parser.
 $source='source '+$sql.Replace('\','/')
 Native (Join-Path $bin 'mariadb.exe') @("--defaults-extra-file=$options","--execute=$source")
 Protect $cfgPath;Protect $licPath
 $env:AIRTRACK_SERVICE_NAME=$ServiceName
 Native (Join-Path $InstallDir 'AirTrack.exe') @('install')
 Native 'sc.exe' @('config',$ServiceName,'depend=','AirTrackDB')
 Start-Service $ServiceName
 $healthy=$false
 for($i=0;$i -lt 90;$i++){
  try{$h=Invoke-RestMethod -Uri ('http://127.0.0.1:'+$appPort+'/updates/api/version') -TimeoutSec 2;if($h.product -eq 'AirTrack-Windows' -and $h.version -eq $ExpectedVersion -and $h.database_ready){$healthy=$true;break}}catch{}
  Start-Sleep -Seconds 1
 }
 if(-not $healthy){throw 'Logbook failed its version/database readiness check; installation is not complete'}
 Write-Output ('Fresh install verified: Logbook '+$ExpectedVersion+', local database ready')
} catch {
 [IO.File]::WriteAllText((Join-Path $dataHome 'fresh-install-error.txt'), $_.Exception.Message, $utf8)
 throw
} finally {
 $rootPassword=$null
 if(Test-Path $private){Remove-Item -LiteralPath $private -Recurse -Force}
}
