# File History: app/templates/header.html
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Released1.0.4: displayed version reads installed release metadata; update access is in Cockpit HUD and Settings, removed from main menu. Native test and main Hayley rendered pages/health/data preservation passed. Installer guard identity aligned; runner now requires completed transaction and exact healthy version before marking installed. Final installer SHA2568fc0e70739c5851501b6b1d7c1d180a452c8c7454c1f3a6d6e392fd6b00ffc28,171897009bytes. Python CI40451460598/source894878c; native correctionscf05983/3306653. Stable/candidate and Workshop use same artifact. Feed expiry2026-11-26T04:56:29.129008Z, ATC calendarID2 updated to15:56AEDT.

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

- 2026-10-27 final1.0.4 acceptance: Corrected the prior claim that version3 was fully visible: health reported3 but app/version.py still displayed1.0.1, header had update link. Source tests14 and CI passed. Initial native candidatec1750084 exposed remaining hardcoded3 guard values; isolated rollback restored healthy3 (Inno returned0, so strengthen runner completion/health verification). Corrected final native upgrade passed config/licence/uploads/weather/aircraft retention and actual rendered4 header, main-menu removal, HUD/Settings links. Main genuine signed SYSTEM3->4 passed rendered pages/database-ready4, original1aircraft digest,16settings and2files unchanged. No fresh wizard/power-cut acceptance claimed. Recovery: retain protected SQL/software transaction snapshots and prior3 Workshop .bak_pre_display_fix_1.0.4_20261027; restore/remove stable pointer to stop new delivery, never automatic downgrade. CalendarID2 expiry updated in place. Source commits894878c,cf05983,3306653; final journals follow.
