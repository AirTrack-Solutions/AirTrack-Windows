# File History: app/app.py
Journal Revision: 1
Last Updated: 2026-10-26

## Current State
2026-10-25 verified outcome: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test.

Imported and registered the existing notam_bp alongside core blueprints. No optional-module scanner dependency; header already shows NOTAMs when endpoint exists.

The database-backed NOTAM blueprint is registered alongside core routes.

## Known Issues
NOTAM page availability verified; full installer wizard/service-mode testing remains pending.

## Future Work
Run a full isolated installer/service-mode test when planned.

## Entry Log
- 2026-10-25: Created before change after actual Hayley test returned404; inspected main blueprint registration, real notam_routes.py and server template. No historical changes inferred.

- 2026-10-25: Imported and registered the existing notam_bp alongside core blueprints. No optional-module scanner dependency; header already shows NOTAMs when endpoint exists. Syntax check passes; rebuilt actual Windows smoke verification pending. Recovery: revert scoped blueprint additions/template. Existing database schema and live Hayley installation unaffected.

- 2026-10-25 final verification: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test. Repaired missing mariadb dependency/collection (767763d), license destination (8eae10e), and unregistered NOTAM blueprint/missing template (1e76b97). Prior runs that passed compilation but failed startup are superseded by this outcome. Final base artifact/recovery is recorded in docs/file_history/AirTrackSetup.exe.md. Test artifacts and private20.9MB source backup retained under C:\Users\trevo\AirTrackTests\notam-20261025 with trevo/SYSTEM/Administrators ACL. No live source data migration, service path change, registry install, app update publication, customer signing/provisioning/email, or external NOTAM API call.

- 2026-10-26: Ported settings-backed METAR display, freshness/fallback/date/layout/name fixes from158 into client. Registered blueprint/menu and added Weather field to existing client Settings panel. Weather station saves validate/normalize codes, allow explicit clearing and preserve existing list if field omitted. NOTAM installer-only choices unchanged. Verification/rebuilt artifact pending. Recovery: revert this scoped commit; retain prior Workshop base until Windows smoke passes.
