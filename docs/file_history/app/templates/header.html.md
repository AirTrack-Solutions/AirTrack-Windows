# File History: app/templates/header.html
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Version/display and Cockpit placement correction 1.0.4 prepared; native verification pending.
2026-10-26: Windows client now includes the settings-backed METAR page and all current158 freshness/name/instrument-layout fixes. Local Weather settings persist station choices; NOTAM installer-only selection remains separate. Frozen timezone data is bundled.

METAR route/menu/template and local weather settings are implemented and verified.

## Known Issues
Compiled application smoke test passed; full installer wizard/service-mode testing remains separate.

## Future Work
Consider full isolated installer/service-mode regression before broad distribution.

## Entry Log
- 2026-10-26: Created before porting Logbook158 METAR display/fixes into Windows V1. No past history inferred.

- 2026-10-26: Ported settings-backed METAR display, freshness/fallback/date/layout/name fixes from158 into client. Registered blueprint/menu and added Weather field to existing client Settings panel. Weather station saves validate/normalize codes, allow explicit clearing and preserve existing list if field omitted. NOTAM installer-only choices unchanged. Verification/rebuilt artifact pending. Recovery: revert this scoped commit; retain prior Workshop base until Windows smoke passes.

- 2026-10-26 verified: Build40298068941 (sourcebaeef32ec3e539ccc1ffc3defb4b8a47c4e0b842) succeeded and its clean compiled bundle passed on Hayley in debug mode against the isolated cloned DB on33317. Verified METAR menu, Settings Weather save/normalization/duplicates/clear/invalid rejection/omitted preservation, live YSWS/YSSY airport cards, local timezone + UTC observation display, no negative instrument offset, and NOTAM six-card/API regressions. No dependency overlays. Original AirTrackClient path/config unchanged (SHA equality), restarted/running; original AirTrackDB/MariaDB running; test app/DB stopped and33317 closed. Full Inno wizard/fresh install/LocalSystem service-mode not exercised. Implementations dfa9700 (METAR/settings), baeef32 (Windows timezone data); source remains on codex/v1-notam-airports-20261025, not merged/published as a release. Earlier timezone-incomplete build superseded/cancelled. New base details and recovery recorded in docs/file_history/AirTrackSetup.exe.md. Existing customer ZIPs/installations unchanged; no automatic rollout or signed app-update publication. Reuse local settings/direct public feeds rather than pointing clients at158/ATC. No additional poller or provider credentials.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-26: Use the runtime version in the visible header instead of hardcoded1.0.0, and run updater signature/route tests before compiling releases. Local suites pass (7 core and3 route tests). Final compiled artifact pending.

- 2026-10-27: Reproduced running service health1.0.3 while compiled version module still fixed1.0.1. Read release metadata for all displayed version values; remove header update link, add Cockpit HUD and Settings access. Bump installer/feed identity1.0.4. Verification pending; retain prior signed1.0.3 and protected snapshots for recovery.
