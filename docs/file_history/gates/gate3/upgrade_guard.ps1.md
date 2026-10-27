# File History: gates/gate3/upgrade_guard.ps1
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Released/deployed1.0.3 on2026-10-27. Main Hayley (.170) bootstrapped to2 and then genuinely upgraded2->3 by the SYSTEM updater from the signed stable feed; database/aircraft/config/settings preservation passed. Native1.0.3 final SHA256c25fd4c9a7bdf8965988a85c70e5bcfd1836dcc21b244f6b9855802e9ca373eb (171899113bytes), native source99007a7 with release data3e78ec2; unchanged Python code from verified build40429896630/ced6ee6. Daily3am task catches up idle/online/onAC, continues if unplugged, supports seven-day postponement, no Windows reboot. See operations/windows_application_updates.md for acceptance and recovery.


## Known Issues
Isolated tests and main deployment passed; protected backups still need administrator review if storage/SQL recovery itself fails.

## Future Work
Implement/verify normal upgrade, abort, failed health and manual crash recovery.

## Entry Log
- 2026-10-26: Created before implementation. Existing installer and Hayley service/config layout read. No prior history inferred.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-26: Windows PowerShell parser passed on Hayley. Strengthened database restore to include DROP/CREATE DATABASE (removes tables introduced by a failed migration), reject conflicting URI/service overrides, and reject a lower-version installer. Recovery is idempotent after a completed rollback. Runtime transaction tests still pending.

- 2026-10-26 Windows runtime: separate AirTrackUpdateTest service starts successfully on5017 against isolated DB33317; original service/config unchanged. First guard Prepare refused before stopping/replacing files due to Windows PowerShell5.1 Split overload resolution. Replaced ambiguous .NET Split calls with PowerShell -split. Re-test pending.

- 2026-10-26 Windows runtime corrections: renamed the application-data variable to avoid PowerShell’s read-only HOME variable; capture the redirected native process handle before waiting so successful MariaDB dumps report a reliable ExitCode. A 20.9MB protected snapshot now completes successfully on Hayley. Earlier failures stopped before replacement and restarted the test application. Deliberate post-replacement failure/restore test running; original laptop service/data not touched.

- 2026-10-26: Deliberate standalone failed-health transaction passed on Hayley: database snapshot restored (including removal of a newly created table), software/config restored, repeated rollback succeeds. Added installer-only deferred rollback: keep service stopped/gated until Inno finishes its own failed-install cleanup, then restore in DeinitializeSetup. This avoids Inno deleting restored files after the guard returns. Full installer negative test pending.

- 2026-10-26: Native full installer safely refused Prepare before replacement (exit7), although direct32-bit and64-bit guard transactions pass. Added protected temporary PowerShell transcript and installer guard exit/path diagnostics to identify this difference; ordinary installer failure/recovery acceptance remains pending. No Workshop/stable release changed.

- 2026-10-27: Implemented automatic-update candidate at Trevor's explicit request. Frozen stage-update CLI exits before external task launches installer. SYSTEM task runs daily3am, catches up when idle10minutes/onAC/network available, never reboots; signed stable feed, seven-day postponement, failed-release hash quarantine. Existing data/backup gate preserved; Rollback can recover missing config after interrupted replacement. Existing installation location fix UsePreviousAppDir=no verified by successful isolated full installer1.0.1. Source tests before build: signature7, automatic policy4, routes3 passed in dependency environment. Pending full new-binary/native task validation and main170 rollout. Recovery disable task AirTrack-Update-<service>, use saved recover.ps1 and transaction state; never bypass gate.

- 2026-10-27: Follow-up1.0.3 will retain AC-only task starts but add DontStopIfGoingOnBatteries so unplugging does not interrupt an in-progress upgrade. Python code unchanged from verified build40429896630; release identity data/native installer advance to1.0.3. This also permits genuine2->3 SYSTEM-task validation after main bootstrap2, instead of relying only on metadata simulation. Native compilation and signed candidate test pending.

- 2026-10-27: Tightened terminal checkpoints before exposing requests: save completed/rolled_back durably before gate removal or restart, so a crash cannot replay a snapshot over later user edits. External runner resumes terminal gate cleanup after version/database health verification, preserving post-completion data. Installer stages the compatible recovery runner outside the program tree after Prepare and before replacement, so an old task can launch recovery after interruption. Candidate1.0.3 is being rebuilt before stable promotion/main2->3 update. Test completed-marker gate cleanup must preserve a SQL marker created after success. Preparing/refused legacy bootstrap may still require administrator recovery after power loss; no trust/gate bypass.

- 2026-10-27 final verification: signature7 + automatic policy4 + route3 tests passed; actual native2/3 upgrade preservation; failed-migration installer rollback; interrupted missing-file recovery; actual SYSTEM terminal gate cleanup retained a post-success SQL marker; genuine signed2->3 SYSTEM update passed on test and main170. Main1aircraft identity/notes,15settings and2existing configuration/runtime files preserved in final trial. Main healthdatabase_ready/version1.0.3, taskSYSTEM/idle/network/AC-only start/stop-on-unplug=false. Validation tasks removed and test app/DB stopped+disabled; original main AirTrackDB/MariaDB running. Workshop5500/5510 detect final base, no customer ZIP/provision/email. Stable/candidate expiry2026-11-26 requires renewed owner publication. Compiled Python unchanged from40429896630; native/data source99007a7/3e78ec2. Recovery uses saved SQL/software/recover.ps1 below C:\ProgramData\AirTrack\updates\backups and active-AirTrackClient.json; installer base backups retained. No true power-cut or fresh wizard test claimed.
