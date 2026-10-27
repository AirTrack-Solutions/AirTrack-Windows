# File History: app/version.py
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Version/display and Cockpit placement correction 1.0.4 prepared; native verification pending.
Existing displayed application version; bump to1.0.1 for updater baseline.

## Known Issues
Baseline update build pending.

## Future Work
Verify compiled identity in Windows.

## Entry Log
- 2026-10-26: Created before V1 updater version changes; existing version module read. No past history inferred.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-27: Reproduced running service health1.0.3 while compiled version module still fixed1.0.1. Read release metadata for all displayed version values; remove header update link, add Cockpit HUD and Settings access. Bump installer/feed identity1.0.4. Verification pending; retain prior signed1.0.3 and protected snapshots for recovery.
