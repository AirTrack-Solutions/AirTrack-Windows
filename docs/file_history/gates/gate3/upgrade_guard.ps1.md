# File History: gates/gate3/upgrade_guard.ps1
Journal Revision: 1
Last Updated: 2026-10-26

## Current State
New external installer guard planned: service stop, protected software/database backups, preservation, health check and recovery. See operations/windows_application_updates.md.

## Known Issues
Must be tested on isolated Windows service/DB, including failures. No production installer publication until then.

## Future Work
Implement/verify normal upgrade, abort, failed health and manual crash recovery.

## Entry Log
- 2026-10-26: Created before implementation. Existing installer and Hayley service/config layout read. No prior history inferred.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-26: Windows PowerShell parser passed on Hayley. Strengthened database restore to include DROP/CREATE DATABASE (removes tables introduced by a failed migration), reject conflicting URI/service overrides, and reject a lower-version installer. Recovery is idempotent after a completed rollback. Runtime transaction tests still pending.
