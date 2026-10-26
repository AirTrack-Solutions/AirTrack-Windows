# File History: .github/workflows/build-windows.yml
Journal Revision: 1
Last Updated: 2026-10-26

## Current State
2026-10-26: Windows client now includes the settings-backed METAR page and all current158 freshness/name/instrument-layout fixes. Local Weather settings persist station choices; NOTAM installer-only selection remains separate. Frozen timezone data is bundled.

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

- 2026-10-26 verified: Build40298068941 (sourcebaeef32ec3e539ccc1ffc3defb4b8a47c4e0b842) succeeded and its clean compiled bundle passed on Hayley in debug mode against the isolated cloned DB on33317. Verified METAR menu, Settings Weather save/normalization/duplicates/clear/invalid rejection/omitted preservation, live YSWS/YSSY airport cards, local timezone + UTC observation display, no negative instrument offset, and NOTAM six-card/API regressions. No dependency overlays. Original AirTrackClient path/config unchanged (SHA equality), restarted/running; original AirTrackDB/MariaDB running; test app/DB stopped and33317 closed. Full Inno wizard/fresh install/LocalSystem service-mode not exercised. Implementations dfa9700 (METAR/settings), baeef32 (Windows timezone data); source remains on codex/v1-notam-airports-20261025, not merged/published as a release. Earlier timezone-incomplete build superseded/cancelled. New base details and recovery recorded in docs/file_history/AirTrackSetup.exe.md. Existing customer ZIPs/installations unchanged; no automatic rollout or signed app-update publication. Reuse local settings/direct public feeds rather than pointing clients at158/ATC. No additional poller or provider credentials.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-26: Candidate build40311359848 compiled Python successfully but Inno rejected a section marker accidentally inserted inside a code comment. Corrected that marker; reuse runner Inno installation when available. No candidate shipped. Route tests additionally passed CSRF rejection, database health, verified delivery and tamper refusal. Rebuild pending.

- 2026-10-26: Use the runtime version in the visible header instead of hardcoded1.0.0, and run updater signature/route tests before compiling releases. Local suites pass (7 core and3 route tests). Final compiled artifact pending.

- 2026-10-26: Original MariaDB download URL now redirects to a website rather than the MSI (confirmed during Hayley build). Changed cold-cache download to official archive.mariadb.org and verify both cached/downloaded MSI against its official sha256sums.txt value4d92fb5f16c0ec8d5a9fc1efdb33a377eaa712d6bce97451e151465c3041ccac. Current compiled Python artifact from build40312824955/source2a9f869 passes all10 updater contract tests. Final installer is being compiled natively on Hayley with source3d1eb2e guard cleanup correction.
