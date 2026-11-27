# Logbook V1 distribution on AirTrack-Windows
Journal Revision: 1
Last Updated: 2026-11-28

## Current State

Hayley Vintage Brass switch rows are 6 px higher with labels beside their switches. The gauges and their labels sit 2 px higher.

Hayley uses the Export 4 Mobile label and an 8 px inner inset on short Vintage Brass viewports.

Hayley uses balanced Windows HUD button banks, with Clean Up on the left. The existing installer predates the change.

Hayley uses shorter Windows Cockpit labels and closer Vintage Brass button spacing on short viewports. The existing installer predates these changes.

Windows 1.1.2 from 5d4345c passed a guarded native upgrade on Hayley and is available as a distribution artifact. The .158 production
browser sign-off accepted the live Chromium hover coverage gap and deferred
user-selectable data text size to V2.

## Entry Log

- 2026-11-27 — Port the signed-off cockpit, Vintage Brass, responsive page,
  Aircraft tooltip and Airlines logo changes from the .158 live inventory at
  6c74037. Explicitly include the tooltip script and theme assets. Retain
  platform-specific templates, CSRF inputs and the Windows frozen theme path.
  Where the target has no community blueprint, omit the unrelated Settings
  link. Regenerate the theme index from each target's own packaged assets.
  Leave unrelated server working-tree changes, private data and backups out.
  Revert the release commit to recover source without changing live .158.

- 2026-11-27 — Source 5d4345c22e1408f8b5380c71470d8c15c225ef56 was
  pushed on release/logbook-v1-20261127. GitHub Actions run 45954530989
  passed updater contracts, PyInstaller, pinned MariaDB MSI verification
  and Inno Setup compilation. The initial cache miss delayed the download;
  the identical commit was fast-forwarded to the existing Windows build
  branch as a fallback. Run 45954530989 recovered and produced the selected
  installer. Verified both Actions ZIP digests, 1.1.2 release metadata,
  and Windows-packaged template, tooltip and Vintage Brass assets against
  source after CRLF normalization. Installer is 181484792 bytes, SHA-256
  8818904b14de4cc65030a715a5b819089ca1b78c124f3dc019e7bd9f0f42ec23.
  No native 1.1.2 upgrade or fresh installation was verified. Stable feed
  and Workshop base stayed on their previous versions. Retain 1.1.1
  and its qualified recovery artifacts for rollback.

- 2026-11-27 — Trevor authorized the native upgrade after seeing Vintage
  Brass on Hayley's 1.1.1 install. Confirmed installer SHA-256 before and after
  transfer, captured protected before/after SQL data snapshots and config and
  licence hashes, then ran Inno in upgrade mode with no reboot. Exit 0;
  transaction completed and HTTP health reports 1.1.2/database_ready.
  All 78 table counts and the complete data snapshot, config and licence
  hashes match across upgrade. Eight served CSS, JS and artwork files match
  1.1.2 source. The actual theme picker refresh retains Vintage Brass and
  Default and the generated CSS imports Vintage Brass. Visual layout in
  Trevor's laptop browser has not been checked. Workshop and stable feed
  were not promoted. Recovery transaction backup on Hayley:
  C:\ProgramData\AirTrack\updates\backups\1514b7613504474387b2be3d6b5e821b.
  Protected verification files are in
  C:\Users\trevo\AirTrackTests\vintage-1.1.2-20261127.

- 2026-11-27 — Trevor reported Vintage Brass HUD labels extending beyond their buttons on Hayley, including Manual Aircraft Entry, Launch Bug Tracker and Application Updates. On viewports up to 1536 px, preserve the 13 px label size and tapered widths, reserve 30 px button height and allow full labels to wrap. The 26 px wide-desktop layout remains. Chromium fixture widths 768, 1024, 1280, 1366, 1536 and 1920 verified equal button heights, no label overflow and both banks entirely in view. Atomically replaced only the installed CSS on Hayley after checking the prior hash. Verified served SHA-256 58d0459c5e515024ea00e08d2d034e055713676c2e5cf04b0aa5ed06a6a4d09c and healthy 1.1.2. No restart. Laptop visual acceptance pending. Original installer does not contain this hotfix. Restore the saved CSS in C:/Users/trevo/AirTrackTests/vintage-1.1.2-20261127/vintage-brass-before-hud.css and hard refresh to recover.

- 2026-11-27 — Trevor requested rolling back the wrapping/height change after the right HUD covered the switches. Restored the pre-hotfix Vintage Brass stylesheet byte-for-byte on Hayley and replaced only the Windows Cockpit labels with Manual Entry, Bug Tracker and Updates. Existing button routes and actions are intact. Verified Jinja parsing, installed template labels and restored served CSS SHA-256 6ac9ffcfd694f807bceee92a4c495973584d019b95ca484a3e8576eb0bf8d4ec; restarted only AirTrackClient and confirmed 1.1.2/database_ready. No visual check in the laptop browser. The base installer predates the label change. Rollback files are admin-before-short-labels.html and vintage-brass-before-label-revert.css under C:/Users/trevo/AirTrackTests/vintage-1.1.2-20261127.

- 2026-11-27 — Trevor said the seven-left/nine-right Windows HUD did not fit the artwork panels as closely as .158. Read-only comparison found byte-identical Vintage CSS and cockpit art. In the Windows stylesheet reduce only the vertical gaps from 6 px to 2 px at viewport heights up to 760 px. Keep the existing 26 px height, 13 px font and shorter labels. Chromium fixture's six windows showed no text overflow, both banks inside the viewport, and clearance above the right switches at all six window sizes. At representative 1239 × 657, clearance from the switch label safety line changed from -13 to +19 px. Hayley served verified SHA-256 f329939342782438615d9f7cd39b8602f126e91fa7c50655cc14540c4cc2dd8a without restart. No direct laptop-browser visual check. The existing installer predates this change. Recovery: restore C:/Users/trevo/AirTrackTests/vintage-1.1.2-20261127/vintage-brass-before-panel-fit.css and hard-refresh.

- 2026-11-27 — Trevor requested balanced HUD banks on Hayley. Move the existing client-only Clean Up button beside the backup controls in the left bank. Verified the Windows template renders eight left and seven static right buttons, plus the runtime Shut Down button for the observed eight-right configuration. The server conditional and existing Clean Up handler are intact. Replaced the installed template with a hash guard, restarted AirTrackClient, and verified 1.1.2/database_ready. Browser visual layout remains to be checked on Hayley. Restore C:/Users/trevo/AirTrackTests/vintage-1.1.2-20261127/admin-before-hud-balance.html and restart AirTrackClient to recover. The existing installer predates the change.

- 2026-11-27 — Trevor marked the brass panels’ inner edges and requested Export 4 Mobile. On short Windows Vintage Brass viewports, inset the inner button edges by another 8 CSS px and set 3 px horizontal padding. Preserve outer alignment, eight-per-bank layout, 26 px height and 13 px text, and the mobile export form action. Jinja parse and six Chromium fixture viewport checks passed, including no overflow and 47 px of right-switch clearance at 1239 × 657. Installed files hash-verified, served CSS SHA-256 86d41ed6f1156f5ecdab6d0cf3d2051f9f3e30cdac6bc73e6419fee22230e062, AirTrackClient restarted and returned version 1.1.2/database_ready. Laptop visual check and installer rebuild pending. Roll back admin-before-export4.html and vintage-brass-before-inset.css from the protected Hayley verification folder, then restart AirTrackClient.

- 2026-11-28 — Trevor requested side labels and a small lift after the lower switch labels appeared over the upper switch row at 1280 × 720. Lifted Vintage Brass Windows click targets and levers together by 4 px. Side labels sit outside each pair; inward labels sit beside their levers on the plates through 900 px to clear gauge text. No event handler or switch sequence change. Chromium geometry fixture passed six viewport sizes including 1243 × 594 (supplied image dimensions), 1280 × 720 and 768 × 1024, checking switch and label overlap with HUD buttons and nearby gauges and gauge text. Guarded CSS-only Hayley replacement served SHA-256 126f384764ca823269ac0f6ff9eeab815f7de3771616a1086416499713940431; no restart. Laptop visual acceptance and installer rebuild pending. Recover by restoring vintage-brass-before-switch-labels.css from the protected Hayley verification directory and hard refreshing.

- 2026-11-28 — Raised the eight Windows Vintage Brass gauges and their attached labels together by 2 CSS px as requested. Chromium fixture checked switch, label and nearby gauge clearance at six viewport sizes. Guarded CSS-only Hayley replacement served SHA-256 88d79366a94813320979a4626752b2a3b4f985e997519ddfc052f31976bb0b75. Laptop visual check and installer rebuild pending. Restore vintage-brass-before-gauge-lift.css from the protected Hayley verification directory to recover.

- 2026-11-28 — Lifted both Vintage Brass switch rows by another 2 CSS px, moving the levers, labels and hit targets together. The gauge lift stays in place. Six viewport fixtures passed switch, label, HUD and nearby gauge clearance checks. Hayley served the guarded CSS replacement with SHA-256 1570ed2c928bd24c6806bf0f518da0eb559aaa31e92954535e3c938cd4b69038 without a restart. Laptop visual check and installer rebuild remain pending. Restore vintage-brass-before-second-switch-lift.css from the protected Hayley verification folder to recover.
