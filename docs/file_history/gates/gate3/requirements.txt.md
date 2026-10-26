# File History: gates/gate3/requirements.txt
Journal Revision: 1
Last Updated: 2026-10-26

## Current State
2026-10-26: Windows client now includes the settings-backed METAR page and all current158 freshness/name/instrument-layout fixes. Local Weather settings persist station choices; NOTAM installer-only selection remains separate. Frozen timezone data is bundled.

2026-10-25 verified outcome: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test.

Windows installer dependencies are pinned here. pyOpenSSL is now pinned to 26.4.0, whose PyPI metadata requires cryptography>=49,<51 and accepts the existing 50.0.0 pin.

## Known Issues
Build run 40188562311 stopped in dependency resolution before compilation.

## Future Work
Verify the retried Windows installer build.

## Entry Log
- 2026-10-25: Created before repairing the build dependency conflict found while implementing V1 NOTAM airport choices. Existing requirements and failed build log read; no historical changes inferred.

- 2026-10-25: Updated only pyOpenSSL 26.3.0 -> 26.4.0 after verifying official PyPI JSON requires_dist metadata. Retained cryptography 50.0.0 rather than downgrade to satisfy the old pin. Recovery: revert this one-line change (which restores the known dependency conflict). Build verification pending.

- 2026-10-25: Build 40188688927 (775d782, branch codex/v1-notam-airports-20261025) passed and artifact installed as the Workshop base. Loader implementation commit fbe5c0b; dependency repair 775d782. Real Windows runtime remains untested. Recovery base and hashes recorded in docs/file_history/AirTrackSetup.exe.md.

- 2026-10-25: Hayley actual startup failed on ModuleNotFoundError mariadb imported by utils/export_mobile_db.py. Added mariadb==1.1.14; official PyPI metadata confirms cp312 win_amd64 wheel. Actual runtime evidence supersedes compile-only readiness. Rebuild pending.

- 2026-10-25 final verification: Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test. Repaired missing mariadb dependency/collection (767763d), license destination (8eae10e), and unregistered NOTAM blueprint/missing template (1e76b97). Prior runs that passed compilation but failed startup are superseded by this outcome. Final base artifact/recovery is recorded in docs/file_history/AirTrackSetup.exe.md. Test artifacts and private20.9MB source backup retained under C:\Users\trevo\AirTrackTests\notam-20261025 with trevo/SYSTEM/Administrators ACL. No live source data migration, service path change, registry install, app update publication, customer signing/provisioning/email, or external NOTAM API call.

- 2026-10-26: Added tzdata2026.5 (version verified via official PyPI JSON) and collect-all tzdata for frozen Windows ZoneInfo support required by METAR observation dates. Existing optional Astral behavior unchanged. Rebuild/actual Windows timezone smoke verification pending. Recovery: revert this scoped addition; retain prior base until tests pass.

- 2026-10-26 verified: Build40298068941 (sourcebaeef32ec3e539ccc1ffc3defb4b8a47c4e0b842) succeeded and its clean compiled bundle passed on Hayley in debug mode against the isolated cloned DB on33317. Verified METAR menu, Settings Weather save/normalization/duplicates/clear/invalid rejection/omitted preservation, live YSWS/YSSY airport cards, local timezone + UTC observation display, no negative instrument offset, and NOTAM six-card/API regressions. No dependency overlays. Original AirTrackClient path/config unchanged (SHA equality), restarted/running; original AirTrackDB/MariaDB running; test app/DB stopped and33317 closed. Full Inno wizard/fresh install/LocalSystem service-mode not exercised. Implementations dfa9700 (METAR/settings), baeef32 (Windows timezone data); source remains on codex/v1-notam-airports-20261025, not merged/published as a release. Earlier timezone-incomplete build superseded/cancelled. New base details and recovery recorded in docs/file_history/AirTrackSetup.exe.md. Existing customer ZIPs/installations unchanged; no automatic rollout or signed app-update publication. Reuse local settings/direct public feeds rather than pointing clients at158/ATC. No additional poller or provider credentials.
