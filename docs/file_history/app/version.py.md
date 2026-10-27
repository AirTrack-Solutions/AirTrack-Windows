# File History: app/version.py
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Released1.0.5: visible label is AirTrack Logbook1.0.5, with Release301/Wilbur removed; FULL_VERSION and SHORT_VERSION use the same installed semantic version. CI40452883616/source40cda52 and actual isolated/main Windows pages passed. Main signed SYSTEM4->5 returned0/statusinstalled5/database_ready;1aircraft,16settings,2files retained. Stable/candidate/Workshop artifact SHA2567b3701a3665a25dd7398b3601e9cb4511e612eecb0b6132c296e3a2ca5e84006,171897691bytes. Signed feed expires2026-11-26T05:07:28.235675Z; calendarID2 updated16:07AEDT.

## Known Issues
None identified in the version/display correction; fresh-install acceptance remains separate.

## Future Work
Keep all future release identities aligned and verify rendered pages as well as health API.

## Entry Log
- 2026-10-26: Created before V1 updater version changes; existing version module read. No past history inferred.

- 2026-10-26: Implemented candidate user-approved Windows application update path: signed release verification/download, Logbook page, version health endpoint, service port support, upgrade transaction guard and installer wiring. Signature/download unit suite passed (7 tests including tampering, expiry, downgrade, truncation and cleanup). Python syntax passed. Windows compilation, service upgrade and failure recovery are pending; candidate is not a production release. Installer upgrade skips database bootstrap, targets the registered service directory, snapshots software/database, blocks requests during migration and checks version/database before clearing the gate. Recovery uses the saved guard/state; no unattended installation. Revert this candidate commit before deployment if validation fails.

- 2026-10-27: Reproduced running service health1.0.3 while compiled version module still fixed1.0.1. Read release metadata for all displayed version values; remove header update link, add Cockpit HUD and Settings access. Bump installer/feed identity1.0.4. Verification pending; retain prior signed1.0.3 and protected snapshots for recovery.

- 2026-10-27 final1.0.4 acceptance: Corrected the prior claim that version3 was fully visible: health reported3 but app/version.py still displayed1.0.1, header had update link. Source tests14 and CI passed. Initial native candidatec1750084 exposed remaining hardcoded3 guard values; isolated rollback restored healthy3 (Inno returned0, so strengthen runner completion/health verification). Corrected final native upgrade passed config/licence/uploads/weather/aircraft retention and actual rendered4 header, main-menu removal, HUD/Settings links. Main genuine signed SYSTEM3->4 passed rendered pages/database-ready4, original1aircraft digest,16settings and2files unchanged. No fresh wizard/power-cut acceptance claimed. Recovery: retain protected SQL/software transaction snapshots and prior3 Workshop .bak_pre_display_fix_1.0.4_20261027; restore/remove stable pointer to stop new delivery, never automatic downgrade. CalendarID2 expiry updated in place. Source commits894878c,cf05983,3306653; final journals follow.

- 2026-10-27: Trevor approved removing the redundant Release301 label. Remove release/name display suffix and use one semantic version for FULL_VERSION/SHORT_VERSION/DISPLAY_VERSION. New package1.0.5 is required for signed updater delivery; installer guard/default/expected version aligned. Source verification and compiled acceptance pending. Prior4 release and snapshots retained for recovery.

- 2026-10-27 release1.0.5: Trevor explicitly approved removal of Release301. Removed redundant release/name display and use one semantic identity; incremented5 so installed4 clients receive signed update. Source identity assertion and14updater checks passed; CI40452883616/source40cda52 full build passed. Exact native header AirTrack Logbook1.0.5 and absence Release301/Wilbur verified on isolated and main HTTPpages, with Cockpit/menu correction retained. Actual main SYSTEM4->5 taskexit0/statusinstalled5 and completed transaction;1aircraft digest,16settings,2files unchanged. Stable/candidate/Workshop share7b3701a3... (171897691bytes). Recovery: protected existing SQL/software transaction snapshots and Workshop .bak_pre_label_cleanup_1.0.5_20261027; restore/remove feed pointer to stop delivery without downgrading clients. Fresh wizard/power-cut not re-tested. CalendarID2 updated in place to26November16:07AEDT after verified signed expiry. Test services stopped/disabled and one-shot/test update tasks removed after acceptance.
