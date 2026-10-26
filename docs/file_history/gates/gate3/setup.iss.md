# File History: gates/gate3/setup.iss
Journal Revision: 1
Last Updated: 2026-10-26

## Current State
2026-10-25 verified outcome: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test.

Installer copies the customer license sidecar into _internal/config, creating that directory first, matching the actual frozen config.license runtime path.

## Known Issues
Actual Windows debug startup logged missing license until the sidecar was copied to the path named in that log. Existing customer license edition semantics are separate and unchanged.

## Future Work
Copy license into actual frozen config path and verify rebuilt artifact.

## Entry Log
- 2026-10-25: Created before correcting the license destination found during authorized Hayley smoke testing. Read installer and app/config/license.py; debug log establishes runtime path. Existing laptop installation not overwritten.

- 2026-10-25: Corrected only the license destination and ensured parent directory creation. In the separately staged test app, copying the existing license to this path changed the runtime result from missing-license fallback to successfully loaded license. No license re-signing or edition changes. Recovery: revert this scoped change. Inno compile verification pending.

- 2026-10-25 final verification: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test. Repaired missing mariadb dependency/collection (767763d), license destination (8eae10e), and unregistered NOTAM blueprint/missing template (1e76b97). Prior runs that passed compilation but failed startup are superseded by this outcome. Final base artifact/recovery is recorded in docs/file_history/AirTrackSetup.exe.md. Test artifacts and private20.9MB source backup retained under C:\Users\trevo\AirTrackTests\notam-20261025 with trevo/SYSTEM/Administrators ACL. No live source data migration, service path change, registry install, app update publication, customer signing/provisioning/email, or external NOTAM API call.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-26: Candidate build40311359848 compiled Python successfully but Inno rejected a section marker accidentally inserted inside a code comment. Corrected that marker; reuse runner Inno installation when available. No candidate shipped. Route tests additionally passed CSRF rejection, database health, verified delivery and tamper refusal. Rebuild pending.
