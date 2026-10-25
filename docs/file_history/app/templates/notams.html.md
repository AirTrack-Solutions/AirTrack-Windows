# File History: app/templates/notams.html
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
2026-10-25 verified outcome: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test.

Added existing Logbook airport-card display and safety footer to Windows, with local jquery-3.7.1.min.js reference; omitted glossary link because Windows has no glossary endpoint. Uses notam_airports from runtime config, not a fixed card count.

Template absent from Windows source; existing database-backed route expects it.

## Known Issues
NOTAM page unavailable in current Windows build.

## Future Work
Wire existing NOTAM page into V1 and verify on Hayley.

## Entry Log
- 2026-10-25: Created before change after actual Hayley test returned404; inspected main blueprint registration, real notam_routes.py and server template. No historical changes inferred.

- 2026-10-25: Added existing Logbook airport-card display and safety footer to Windows, with local jquery-3.7.1.min.js reference; omitted glossary link because Windows has no glossary endpoint. Uses notam_airports from runtime config, not a fixed card count. Syntax check passes; rebuilt actual Windows smoke verification pending. Recovery: revert scoped blueprint additions/template. Existing database schema and live Hayley installation unaffected.

- 2026-10-25 final verification: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test. Repaired missing mariadb dependency/collection (767763d), license destination (8eae10e), and unregistered NOTAM blueprint/missing template (1e76b97). Prior runs that passed compilation but failed startup are superseded by this outcome. Final base artifact/recovery is recorded in docs/file_history/AirTrackSetup.exe.md. Test artifacts and private20.9MB source backup retained under C:\Users\trevo\AirTrackTests\notam-20261025 with trevo/SYSTEM/Administrators ACL. No live source data migration, service path change, registry install, app update publication, customer signing/provisioning/email, or external NOTAM API call.
