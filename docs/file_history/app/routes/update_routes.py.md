# File History: app/routes/update_routes.py
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Released/deployed1.0.3 on2026-10-27. Main Hayley (.170) bootstrapped to2 and then genuinely upgraded2->3 by the SYSTEM updater from the signed stable feed; database/aircraft/config/settings preservation passed. Native1.0.3 final SHA256c25fd4c9a7bdf8965988a85c70e5bcfd1836dcc21b244f6b9855802e9ca373eb (171899113bytes), native source99007a7 with release data3e78ec2; unchanged Python code from verified build40429896630/ced6ee6. Daily3am task catches up idle/online/onAC, continues if unplugged, supports seven-day postponement, no Windows reboot. See operations/windows_application_updates.md for acceptance and recovery.


## Known Issues
Implementation and Windows upgrade/runtime validation complete; see operations journal for limits.

## Future Work
Retain release artifacts/recovery snapshots; publish and sign each future validated release.

## Entry Log
- 2026-10-26: Created before implementation under authorized V1 user-approved update scope; see operations/windows_application_updates.md for design/recovery. No past history inferred.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-26: Health check now verifies required logbook tables and all bundled migrations, because the legacy migration runner logs errors without re-raising. A failed or pending migration must not appear as a successful upgrade. Compiled runtime validation pending.

- 2026-10-27: Implemented automatic-update candidate at Trevor's explicit request. Frozen stage-update CLI exits before external task launches installer. SYSTEM task runs daily3am, catches up when idle10minutes/onAC/network available, never reboots; signed stable feed, seven-day postponement, failed-release hash quarantine. Existing data/backup gate preserved; Rollback can recover missing config after interrupted replacement. Existing installation location fix UsePreviousAppDir=no verified by successful isolated full installer1.0.1. Source tests before build: signature7, automatic policy4, routes3 passed in dependency environment. Pending full new-binary/native task validation and main170 rollout. Recovery disable task AirTrack-Update-<service>, use saved recover.ps1 and transaction state; never bypass gate.

- 2026-10-27 final verification: signature7 + automatic policy4 + route3 tests passed; actual native2/3 upgrade preservation; failed-migration installer rollback; interrupted missing-file recovery; actual SYSTEM terminal gate cleanup retained a post-success SQL marker; genuine signed2->3 SYSTEM update passed on test and main170. Main1aircraft identity/notes,15settings and2existing configuration/runtime files preserved in final trial. Main healthdatabase_ready/version1.0.3, taskSYSTEM/idle/network/AC-only start/stop-on-unplug=false. Validation tasks removed and test app/DB stopped+disabled; original main AirTrackDB/MariaDB running. Workshop5500/5510 detect final base, no customer ZIP/provision/email. Stable/candidate expiry2026-11-26 requires renewed owner publication. Compiled Python unchanged from40429896630; native/data source99007a7/3e78ec2. Recovery uses saved SQL/software/recover.ps1 below C:\ProgramData\AirTrack\updates\backups and active-AirTrackClient.json; installer base backups retained. No true power-cut or fresh wizard test claimed.
