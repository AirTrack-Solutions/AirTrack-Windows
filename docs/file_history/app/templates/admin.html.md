# File History: app/templates/admin.html
Journal Revision: 1
Last Updated: 2026-11-27

## Current State

Hayley uses the Export 4 Mobile label and an 8 px inner inset on short Vintage Brass viewports.

Hayley uses balanced Windows HUD button banks, with Clean Up on the left. The existing installer predates the change.

Hayley uses the original Vintage Brass button geometry and the shorter Windows Cockpit labels. The existing installer predates the label change.

Ported the signed-off Logbook V1 responsive and Vintage Brass release work to this target. See the V1 distribution journal for scope, verification and recovery.
Released1.0.4: displayed version reads installed release metadata; update access is in Cockpit HUD and Settings, removed from main menu. Native test and main Hayley rendered pages/health/data preservation passed. Installer guard identity aligned; runner now requires completed transaction and exact healthy version before marking installed. Final installer SHA2568fc0e70739c5851501b6b1d7c1d180a452c8c7454c1f3a6d6e392fd6b00ffc28,171897009bytes. Python CI40451460598/source894878c; native correctionscf05983/3306653. Stable/candidate and Workshop use same artifact. Feed expiry2026-11-26T04:56:29.129008Z, ATC calendarID2 updated to15:56AEDT.

## Known Issues
Compiled application smoke test passed; full installer wizard/service-mode testing remains separate.

## Future Work
Consider full isolated installer/service-mode regression before broad distribution.

## Entry Log
- 2026-10-26: Created before porting Logbook158 METAR display/fixes into Windows V1. No past history inferred.

- 2026-10-26: Ported settings-backed METAR display, freshness/fallback/date/layout/name fixes from158 into client. Registered blueprint/menu and added Weather field to existing client Settings panel. Weather station saves validate/normalize codes, allow explicit clearing and preserve existing list if field omitted. NOTAM installer-only choices unchanged. Verification/rebuilt artifact pending. Recovery: revert this scoped commit; retain prior Workshop base until Windows smoke passes.

- 2026-10-26 verified: Build40298068941 (sourcebaeef32ec3e539ccc1ffc3defb4b8a47c4e0b842) succeeded and its clean compiled bundle passed on Hayley in debug mode against the isolated cloned DB on33317. Verified METAR menu, Settings Weather save/normalization/duplicates/clear/invalid rejection/omitted preservation, live YSWS/YSSY airport cards, local timezone + UTC observation display, no negative instrument offset, and NOTAM six-card/API regressions. No dependency overlays. Original AirTrackClient path/config unchanged (SHA equality), restarted/running; original AirTrackDB/MariaDB running; test app/DB stopped and33317 closed. Full Inno wizard/fresh install/LocalSystem service-mode not exercised. Implementations dfa9700 (METAR/settings), baeef32 (Windows timezone data); source remains on codex/v1-notam-airports-20261025, not merged/published as a release. Earlier timezone-incomplete build superseded/cancelled. New base details and recovery recorded in docs/file_history/AirTrackSetup.exe.md. Existing customer ZIPs/installations unchanged; no automatic rollout or signed app-update publication. Reuse local settings/direct public feeds rather than pointing clients at158/ATC. No additional poller or provider credentials.

- 2026-10-27: Reproduced running service health1.0.3 while compiled version module still fixed1.0.1. Read release metadata for all displayed version values; remove header update link, add Cockpit HUD and Settings access. Bump installer/feed identity1.0.4. Verification pending; retain prior signed1.0.3 and protected snapshots for recovery.

- 2026-10-27 final1.0.4 acceptance: Corrected the prior claim that version3 was fully visible: health reported3 but app/version.py still displayed1.0.1, header had update link. Source tests14 and CI passed. Initial native candidatec1750084 exposed remaining hardcoded3 guard values; isolated rollback restored healthy3 (Inno returned0, so strengthen runner completion/health verification). Corrected final native upgrade passed config/licence/uploads/weather/aircraft retention and actual rendered4 header, main-menu removal, HUD/Settings links. Main genuine signed SYSTEM3->4 passed rendered pages/database-ready4, original1aircraft digest,16settings and2files unchanged. No fresh wizard/power-cut acceptance claimed. Recovery: retain protected SQL/software transaction snapshots and prior3 Workshop .bak_pre_display_fix_1.0.4_20261027; restore/remove stable pointer to stop new delivery, never automatic downgrade. CalendarID2 expiry updated in place. Source commits894878c,cf05983,3306653; final journals follow.

- 2026-11-22 before edit: Trevor authorises community sharing/downloadableLogbook. Port qualified native client feature with defaults-off/local consent, metadata/credit retention, own-db matches and ATC review. Preserve Windows native service/updater/Weather hooks. Candidate release1.1.0; build artifact first, no stable feed switch until qualification.

- 2026-11-22 candidate source ready: default-off community settings/manual-sharing/own-DB reg+MSN+type+hex matching, fresh contributor approval gate, missing-only downloads, metadata and embedded credit/licence retention, portable local locks/private backup state. Explicit native source deltas retain updater/service/Weather. Twelve community and nine metadata tests pass in isolated153Python3.11/Pillow13 runtime (not a native Windows claim). Additional hidden imports and CI regressions added. Candidate1.1.0, stable feed/base installer remains1.0.5 until compiled qualification. Recover by reverting candidate source only; no Windows data changed.

- 2026-11-27 — Ported the signed-off Logbook V1 responsive and Vintage Brass release work to this target. See the V1 distribution journal for scope, verification and recovery.

- 2026-11-27 — Trevor requested rolling back the wrapping/height change after the right HUD covered the switches. Restored the pre-hotfix Vintage Brass stylesheet byte-for-byte on Hayley and replaced only the Windows Cockpit labels with Manual Entry, Bug Tracker and Updates. Existing button routes and actions are intact. Verified Jinja parsing, installed template labels and restored served CSS SHA-256 6ac9ffcfd694f807bceee92a4c495973584d019b95ca484a3e8576eb0bf8d4ec; restarted only AirTrackClient and confirmed 1.1.2/database_ready. No visual check in the laptop browser. The base installer predates the label change. Rollback files are admin-before-short-labels.html and vintage-brass-before-label-revert.css under C:/Users/trevo/AirTrackTests/vintage-1.1.2-20261127.

- 2026-11-27 — Trevor requested balanced HUD banks on Hayley. Move the existing client-only Clean Up button beside the backup controls in the left bank. Verified the Windows template renders eight left and seven static right buttons, plus the runtime Shut Down button for the observed eight-right configuration. The server conditional and existing Clean Up handler are intact. Replaced the installed template with a hash guard, restarted AirTrackClient, and verified 1.1.2/database_ready. Browser visual layout remains to be checked on Hayley. Restore C:/Users/trevo/AirTrackTests/vintage-1.1.2-20261127/admin-before-hud-balance.html and restart AirTrackClient to recover. The existing installer predates the change.

- 2026-11-27 — Trevor marked the brass panels’ inner edges and requested Export 4 Mobile. On short Windows Vintage Brass viewports, inset the inner button edges by another 8 CSS px and set 3 px horizontal padding. Preserve outer alignment, eight-per-bank layout, 26 px height and 13 px text, and the mobile export form action. Jinja parse and six Chromium fixture viewport checks passed, including no overflow and 47 px of right-switch clearance at 1239 × 657. Installed files hash-verified, served CSS SHA-256 86d41ed6f1156f5ecdab6d0cf3d2051f9f3e30cdac6bc73e6419fee22230e062, AirTrackClient restarted and returned version 1.1.2/database_ready. Laptop visual check and installer rebuild pending. Roll back admin-before-export4.html and vintage-brass-before-inset.css from the protected Hayley verification folder, then restart AirTrackClient.
