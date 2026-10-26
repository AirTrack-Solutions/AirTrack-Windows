# File History: .github/workflows/build-windows.yml
Journal Revision: 1
Last Updated: 2026-10-26

## Current State
2026-10-25 verified outcome: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test.

Windows workflow compiles PyInstaller application and Inno Setup installer, uploads installer and a separate AirTrack-application bundle (14-day retention).

## Known Issues
Installer cannot be extracted by available innoextract version, and running it on Hayley would affect the existing service/database.

## Future Work
Validate artifact and isolated Windows startup.

## Entry Log
- 2026-10-25: Created before adding compiled-app artifact. Existing workflow read; no historical changes inferred.

- 2026-10-25: Added compiled application artifact without credentials/config/license sidecars, allowing smoke testing away from existing installations. Installer build/release steps unchanged. Recovery: remove added upload step. Workflow dispatched on feature branch; verification pending.

- 2026-10-25: Added --collect-all mariadb to carry connector package/native dependencies into frozen app after actual Windows smoke test exposed missing import. Application-artifact build40189455445 had succeeded but runtime failed. Rebuild pending.

- 2026-10-25 final verification: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test. Repaired missing mariadb dependency/collection (767763d), license destination (8eae10e), and unregistered NOTAM blueprint/missing template (1e76b97). Prior runs that passed compilation but failed startup are superseded by this outcome. Final base artifact/recovery is recorded in docs/file_history/AirTrackSetup.exe.md. Test artifacts and private20.9MB source backup retained under C:\Users\trevo\AirTrackTests\notam-20261025 with trevo/SYSTEM/Administrators ACL. No live source data migration, service path change, registry install, app update publication, customer signing/provisioning/email, or external NOTAM API call.

- 2026-10-26: Added tzdata2026.5 (version verified via official PyPI JSON) and collect-all tzdata for frozen Windows ZoneInfo support required by METAR observation dates. Existing optional Astral behavior unchanged. Rebuild/actual Windows timezone smoke verification pending. Recovery: revert this scoped addition; retain prior base until tests pass.
