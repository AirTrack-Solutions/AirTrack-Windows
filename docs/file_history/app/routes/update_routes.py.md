# File History: app/routes/update_routes.py
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
2026-10-27 candidate in progress: signed staging CLI plus independent SYSTEM daily/idle/on-AC task; seven-day postponement, pre-install hash recheck, existing transaction backups/rollback and interrupted-state recovery. Release identity1.0.2. Full Windows validation pending; no customer publication yet.

New file planned: User-approved check/prepare/download page; never execute an installer from Flask.

## Known Issues
Implementation and verification pending.

## Future Work
Complete tests and end-to-end upgrade validation before release.

## Entry Log
- 2026-10-26: Created before implementation under authorized V1 user-approved update scope; see operations/windows_application_updates.md for design/recovery. No past history inferred.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-26: Health check now verifies required logbook tables and all bundled migrations, because the legacy migration runner logs errors without re-raising. A failed or pending migration must not appear as a successful upgrade. Compiled runtime validation pending.

- 2026-10-27: Implemented automatic-update candidate at Trevor's explicit request. Frozen stage-update CLI exits before external task launches installer. SYSTEM task runs daily3am, catches up when idle10minutes/onAC/network available, never reboots; signed stable feed, seven-day postponement, failed-release hash quarantine. Existing data/backup gate preserved; Rollback can recover missing config after interrupted replacement. Existing installation location fix UsePreviousAppDir=no verified by successful isolated full installer1.0.1. Source tests before build: signature7, automatic policy4, routes3 passed in dependency environment. Pending full new-binary/native task validation and main170 rollout. Recovery disable task AirTrack-Update-<service>, use saved recover.ps1 and transaction state; never bypass gate.
