#ifndef ReleaseVersion
  #error ReleaseVersion is required. Run compile_installer.ps1.
#endif

; AirTrack Windows Installer
; Gate 3 - full installer with per-customer config
;
; BUILD:
;   Automated via .github/workflows/build-windows.yml
;   Requires mariadb-11.4.12-winx64.msi in gates\gate3\ at build time
;
; DEPLOY:
;   AirTrack-Admin packages AirTrackSetup.exe + airtrack.cfg + license.lic
;   Customer extracts zip and runs AirTrackSetup.exe

[Setup]
AppName=AirTrack
AppVersion={#ReleaseVersion}
DefaultDirName={code:InstallDirectory}
UsePreviousAppDir=no
DisableDirPage=yes
DisableProgramGroupPage=yes
OutputBaseFilename=AirTrackSetup
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin
CreateUninstallRegKey=no
Uninstallable=no

[Files]
; MariaDB MSI - bundled, extracted to temp and deleted after install
Source: "mariadb-11.4.12-winx64.msi"; DestDir: "{tmp}"; Flags: deleteafterinstall

; MariaDB readiness check
Source: "upgrade_guard.ps1"; Flags: dontcopy
Source: "automatic_updates.ps1"; Flags: dontcopy

Source: "install_fresh.ps1"; Flags: dontcopy

; AirTrack schema - used on fresh installs only
Source: "schema.sql"; DestDir: "{tmp}"; Flags: deleteafterinstall

; AirTrack bundle (built by build.bat / GitHub Actions)
Source: "dist\AirTrack\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[InstallDelete]
Type: filesandordirs; Name: "{app}\_internal"; Check: IsUpgrade
Type: files; Name: "{app}\AirTrack.exe"; Check: IsUpgrade

[Run]
; Step 7 - Open browser (interactive installs only)
Filename: "http://localhost:5000"; Flags: shellexec nowait postinstall skipifsilent; Description: "Open AirTrack in browser"

[Code]
var
  UpgradeInstall, UpgradePrepared, UpgradeFinished: Boolean;
  AppService, TransactionFile: String;

procedure RegisterAutomaticUpdates();
var Home, Params: String; Code: Integer;
begin
  Home := GetIniString('app', 'data_dir', ExpandConstant('{commonappdata}\AirTrack'), ExpandConstant('{app}\airtrack.cfg'));
  ExtractTemporaryFile('automatic_updates.ps1');
  Params := '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + ExpandConstant('{tmp}\automatic_updates.ps1') + '" -Mode Register -InstallDir "' + ExpandConstant('{app}') + '" -DataDir "' + Home + '" -ServiceName "' + AppService + '"';
  if not Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'), Params, '', SW_HIDE, ewWaitUntilTerminated, Code) or (Code <> 0) then
    Log('WARNING: Logbook is installed but automatic update scheduling could not be enabled. Re-run the installer to repair scheduling.');
end;

function IsUpgrade: Boolean;
begin
  Result := UpgradeInstall;
end;

function IsFresh: Boolean;
begin
  Result := not UpgradeInstall;
end;

function InstallDirectory(Param: String): String;
var ImagePath: String; P: Integer;
begin
  Result := 'C:\AirTrack';
  AppService := ExpandConstant('{param:SERVICENAME|AirTrackClient}');
  if RegQueryStringValue(HKLM, 'SYSTEM\CurrentControlSet\Services\' + AppService, 'ImagePath', ImagePath) then
  begin
    if Copy(ImagePath, 1, 1) <> '"' then RaiseException('Existing service has an unsupported unquoted executable path.');
    Delete(ImagePath, 1, 1);
    P := Pos('"', ImagePath);
    if P = 0 then RaiseException('Cannot determine existing service location.');
    Result := ExtractFileDir(Copy(ImagePath, 1, P-1));
  end;
end;

function RunGuard(Mode: String): Boolean;
var Code: Integer; Params: String; Diagnostic: AnsiString;
begin
  Params := '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + ExpandConstant('{tmp}\upgrade_guard.ps1') + '" -Mode ' + Mode + ' -InstallDir "' + ExpandConstant('{app}') + '" -ServiceName "' + AppService + '" -ExpectedVersion {#ReleaseVersion} -StateFile "' + TransactionFile + '"';
  Params := Params + ' -DiagnosticsPath "' + ExpandConstant('{tmp}\upgrade-guard.log') + '"';
  Log('Upgrade guard ' + Mode + ': ' + Params);
  if Mode = 'Finish' then Params := Params + ' -DeferRollback';
  Result := Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'), Params, '', SW_HIDE, ewWaitUntilTerminated, Code) and (Code = 0);
  Log('Upgrade guard exit: ' + IntToStr(Code));
  if LoadStringFromFile(ExpandConstant('{tmp}\upgrade-guard.log'), Diagnostic) then Log(String(Diagnostic));
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var Home, Cfg: String;
begin
  Result := '';
  if ExpandConstant('{param:RELEASEVERSION|{#ReleaseVersion}}') <> '{#ReleaseVersion}' then
  begin
    Result := 'The signed release version does not match this installer. Nothing was changed.';
    Exit;
  end;
  UpgradeInstall := RegKeyExists(HKLM, 'SYSTEM\CurrentControlSet\Services\' + AppService);
  if UpgradeInstall then
  begin
    Cfg := ExpandConstant('{app}\airtrack.cfg');
    Home := GetIniString('app', 'data_dir', ExpandConstant('{commonappdata}\AirTrack'), Cfg);
    TransactionFile := AddBackslash(Home) + 'updates\active-' + AppService + '.json';
    ExtractTemporaryFile('upgrade_guard.ps1');
    if RunGuard('Prepare') then
    begin
      UpgradePrepared := True;
      // Preserve recovery control outside the program tree before replacement.
      // An existing scheduled task can recover even if power fails before
      // the final task registration or gate cleanup.
      ExtractTemporaryFile('automatic_updates.ps1');
      if not FileCopy(ExpandConstant('{tmp}\automatic_updates.ps1'), AddBackslash(Home) + 'updates\automatic_updates.ps1', False) then
        Result := 'Could not preserve the recovery runner. Installation stopped.';
    end
    else Result := 'AirTrack could not create a verified backup. Installation has been stopped. See the protected updates folder in the application data directory.';
  end
  else if not FileExists(ExpandConstant('{src}\airtrack.cfg')) or not FileExists(ExpandConstant('{src}\license.lic')) then
    Result := 'Extract the complete customer package first. Keep airtrack.cfg and license.lic beside AirTrackSetup.exe.'
  else if (AppService <> 'AirTrackClient') or FileExists(ExpandConstant('{app}\airtrack.cfg')) then
    Result := 'No matching service exists. This installation needs a manual review before replacement.';
end;

procedure DeinitializeSetup();
begin
  if UpgradePrepared and (not UpgradeFinished) then
    if not RunGuard('Rollback') then
      MsgBox('Automatic recovery did not complete. Keep AirTrack stopped and use recover.ps1 in the protected update backup folder.', mbError, MB_OK);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  LicSrc, LicDest, Params: String;
  Code: Integer;
begin
  { Configure copied files before post-install service actions. }
  if CurStep = ssPostInstall then
  begin
    if UpgradeInstall then
    begin
      if not RunGuard('Finish') then
        RaiseException('AirTrack upgrade failed. Recovery was attempted; inspect the protected update transaction before retrying.');
      UpgradeFinished := True;
      RegisterAutomaticUpdates();
      Exit;
    end;
    { Copy sidecar airtrack.cfg - preserve on reinstall }
    if not FileExists(ExpandConstant('{app}\airtrack.cfg')) then
      FileCopy(ExpandConstant('{src}\airtrack.cfg'), ExpandConstant('{app}\airtrack.cfg'), False);

    { Copy sidecar license.lic }
    LicSrc  := ExpandConstant('{src}\license.lic');
    LicDest := ExpandConstant('{app}\_internal\config\license.lic');
    ForceDirectories(ExtractFileDir(LicDest));
    if FileExists(LicSrc) then
      FileCopy(LicSrc, LicDest, False);

    { Create runtime data directory structure }
    CreateDir('C:\ProgramData\AirTrack');
    CreateDir('C:\ProgramData\AirTrack\logs');
    CreateDir('C:\ProgramData\AirTrack\backups');
    CreateDir('C:\ProgramData\AirTrack\core');
    CreateDir('C:\ProgramData\AirTrack\packages');

    { Copy core verification files from bundle }
    FileCopy(
      ExpandConstant('{app}\_internal\app\core\airtrack_solutions.pub'),
      'C:\ProgramData\AirTrack\core\airtrack_solutions.pub', False
    );
    FileCopy(
      ExpandConstant('{app}\_internal\app\core\package_installer.py'),
      'C:\ProgramData\AirTrack\core\package_installer.py', False
    );
    ExtractTemporaryFile('install_fresh.ps1');
    Params := '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + ExpandConstant('{tmp}\install_fresh.ps1') + '" -InstallDir "' + ExpandConstant('{app}') + '" -MsiPath "' + ExpandConstant('{tmp}\mariadb-11.4.12-winx64.msi') + '" -SchemaPath "' + ExpandConstant('{tmp}\schema.sql') + '" -ExpectedVersion "{#ReleaseVersion}" -ServiceName "' + AppService + '"';
    if not Exec(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe'), Params, '', SW_HIDE, ewWaitUntilTerminated, Code) or (Code <> 0) then
      RaiseException('Fresh installation failed its database/service readiness checks. Installation is not complete. Contact AirTrack before retrying.');
    RegisterAutomaticUpdates();
  end;
end;
