# Windows V1 application updates

Status: automatic-update candidate1.0.2 under Windows validation, 2026-10-27. Do not treat compilation as release approval.

New installations register `AirTrack-Update-AirTrackClient`, a SYSTEM scheduled task. It checks the signed stable release feed daily at3am and catches up when Windows is idle for ten minutes, online and on AC power. It does not wake or reboot the computer. The frozen `stage-update` command verifies and downloads the release, then exits before a separate PowerShell runner starts the silent installer, avoiding frozen-file locks. Existing transactions requiring recovery are rolled back before any new release is attempted. Failed release hashes are quarantined until a corrected release is published; an administrator can inspect/recover and remove `updates/failed-release.json` to retry deliberately.

Logbook's Application updates page shows the last check/status and allows postponing automatic updates for seven days or resuming them. Manual verified installer download remains available. Older clients require one bootstrap upgrade; future releases use the installed task. A fresh owner release still requires a compiled and verified installer plus signed publication. Updating the Workshop base alone does not upgrade installed clients.

To disable the mechanism administratively, disable the named scheduled task. Preserve recovery files. The runner is in the protected application-data updates folder; installing it requires administrator approval once. No interactive installer is launched from the application service. Scheduling failure is logged after a completed upgrade rather than triggering unsafe installer cleanup of already-verified application files; re-run the installer to repair scheduling.

## Upgrade transaction

The installer locates the existing AirTrackClient executable from the Windows service registration, rather than assuming C:\AirTrack. An existing configuration without a matching service is refused. An upgrade skips MariaDB installation/bootstrap, stops the application, secures a recovery directory below the configured application data folder and creates both a full software snapshot and a database dump before file replacement.

During upgrade verification, a persistent update gate refuses application requests and suspends capability delivery. The version endpoint requires the expected application version, working logbook tables and every bundled SQL migration. Only a successful check removes the gate. A normal failure restores the database and application snapshot and restarts the previous service. Local settings, licence and embedded upload/runtime folders are preserved; data outside the program directory remains in place.

Supported automatic upgrade preconditions: local database; individual database fields matching the configured URI; no conflicting service environment overrides; quoted registered executable path; application data folder outside the program directory; no linked/reparse installation files. Other layouts are refused before replacement for manual review. Use a backup account that can dump and restore the whole application database, including DROP/CREATE DATABASE. App writes are stopped while taking the snapshot; external DB writers must also be paused.

## Owner release publication

Wombat implementation is on .153 at /home/airtrack/docker/AirTrack-Wombat. The dedicated endpoints are /api/wombat/windows-release, /api/wombat/windows-release/candidate and /api/wombat/windows-installers/<version>/<sha256>.exe. These routes cannot sign or publish releases. The existing template-overlay updater remains separate.

After compiling and validating a release, run bin/publish_windows_release.py locally on Wombat with --root, --installer, --version, --public-key and --notes-file. The private signing key stays on Wombat; --public-key must be the Windows bundled trust root. Default publication is **candidate**, which normal clients do not use. Validate signed HTTPS retrieval with a test client before explicitly publishing --channel stable. Version/hash URLs are immutable in normal use; retain prior artifacts for recovery. Metadata expires (default30 days); the owner must renew the signed feed before expiry using a reviewed installer, rather than removing expiry validation.

The signature domain is “AirTrack Windows installer release v1” followed by a newline and canonical sorted compact ASCII JSON. Manifest fields bind product, version, URL, SHA256, size, publication/expiry and release notes. Downloaded installer integrity follows from this signature; Windows may still show its normal publisher/SmartScreen prompt because this is separate from Authenticode signing.

## Recovery

Recovery snapshots contain sensitive data and are ACL-restricted to SYSTEM/Administrators. Retain them until the updated application has been checked; they are not automatically deleted. The active state file is <application-data>\updates\active-AirTrackClient.json. Each backup contains recover.ps1, application\ and database.sql. Never share these files publicly.

On interrupted installation, leave the application stopped. Open an administrator PowerShell window, inspect the active state and run the saved recover.ps1 with -Mode Rollback, -InstallDir set to the recorded installation folder, -ServiceName AirTrackClient and -StateFile set to the active transaction file. A preparing state restarts the untouched old application; prepared/checking states restore software and database. Completed/rolled_back states must not be rolled back through a different snapshot without manual review. Do not delete the update gate to bypass incomplete recovery.

The installer handles ordinary errors and cancellation; abrupt power loss requires this recovery procedure. Database restoration cannot protect against unrelated external writers or failing storage. A failure while restoring leaves the gate/state for investigation rather than falsely claiming success.

## Isolated Windows acceptance tests

Use a separate application service (AirTrackUpdateTest), application port5017, private data folder and cloned database on33317. Installer /SERVICENAME=AirTrackUpdateTest is an administrator test override. Do not alter the original AirTrackClient service path/config or its database. Test signed download, real installer upgrade, licence/config/uploads/settings preservation, failed health/migration rollback including removal of newly introduced tables, and cleanup of temporary services/ports. Record exact build/source/hash and results in the engineering journal before changing the Workshop base or stable feed.
