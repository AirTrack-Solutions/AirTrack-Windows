# File History: gates/gate3/service.py
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
2026-10-25 verified outcome: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test.

Windows service reads per-customer airtrack.cfg before importing Flask. The [notams] airports setting is validated and loaded into NOTAM_PRIMARY_AIRPORTS and NOTAM_HOME_ICAOS before importing Flask. Legacy configs retain original four airports.

## Known Issues
Existing compiled installers require rebuilding to include Python service changes.

## Future Work
Verify rebuilt installer on a real Windows installation.

## Entry Log
- 2026-10-25: Created before adding NOTAM configuration support; inspected _load_config and installer build workflow. No prior history inferred.

- 2026-10-25: Added V1 per-package NOTAM airport configuration at Trevor request. One to six distinct ASCII four-letter codes; malformed config fails explicitly; existing process environment overrides retained. Actual _load_config tested with generated sidecar configs for one and six airports; syntax passes. No real Windows runtime test yet. Compiled base requires rebuild. Recovery: revert the loader change or restore previous base installer; existing configs without [notams] continue to work.

- 2026-10-25: Build 40188688927 (775d782, branch codex/v1-notam-airports-20261025) passed and artifact installed as the Workshop base. Loader implementation commit fbe5c0b; dependency repair 775d782. Real Windows runtime remains untested. Recovery base and hashes recorded in docs/file_history/AirTrackSetup.exe.md.

- 2026-10-25 final verification: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test. Repaired missing mariadb dependency/collection (767763d), license destination (8eae10e), and unregistered NOTAM blueprint/missing template (1e76b97). Prior runs that passed compilation but failed startup are superseded by this outcome. Final base artifact/recovery is recorded in docs/file_history/AirTrackSetup.exe.md. Test artifacts and private20.9MB source backup retained under C:\Users\trevo\AirTrackTests\notam-20261025 with trevo/SYSTEM/Administrators ACL. No live source data migration, service path change, registry install, app update publication, customer signing/provisioning/email, or external NOTAM API call.
