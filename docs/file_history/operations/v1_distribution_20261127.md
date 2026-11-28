# Logbook V1 distribution on AirTrack-Windows
Journal Revision: 1
Last Updated: 2026-11-28 Australia/Sydney

## Current State

Windows 1.1.5 candidate passed native fresh and upgrade checks. Cross-platform restore remains open.

Windows 1.1.4 fixes the native restore command and is installed on Hayley.

Installer Workshop now uses native-qualified Windows 1.1.3 for new customer ZIPs.

Windows 1.1.3 is packaged and passed the native upgrade on Hayley with the approved Cockpit layout.

Hayley Vintage Brass switch rows are 6 px higher with labels beside their switches. The gauges and their labels sit 4 px higher.

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

- 2026-11-28 — Raised the eight Windows Vintage Brass gauges and attached labels another 2 CSS px. Six Chromium fixtures passed nearby gauge, switch and HUD clearance checks. Guarded CSS-only replacement on Hayley served SHA-256 e379c4485b81a6ae79352daad036b2af0d0038fa7faa7418cbd58fad60a01f3f without restart. Direct visual acceptance and installer rebuild pending. Restore vintage-brass-before-second-gauge-lift.css from the protected Hayley verification folder to recover.

- 2026-11-28 — Trevor approved the final Hayley layout and requested packaging. Advance the Windows installer identity to 1.1.3 so it can be distinguished from the original 1.1.2 installer. The approved layout is in 6a5a766. Build and artifact verification pending. Retain the previous installer for recovery.

- 2026-11-28 — Windows 1.1.3 packaging completed from b9a4a9b96afeba8c2c59c7334e7d0d0166d62c25. GitHub Actions 46004365508 passed updater contract tests, compiled the app, verified the pinned MariaDB MSI and built the Inno installer. Verified both artifact ZIP digests and Windows release metadata, templates, styles, tooltip/shutdown scripts and artwork against source. The Cockpit template and Vintage Brass CSS match the approved files on Hayley. Installer 181483706 bytes, SHA-256 fccc6af3df649b5827930cf6e024893a41e41eaa64df5467feb72b211986eeff. No native 1.1.3 install, Workshop promotion or stable feed update. Keep the previous qualified installer and Hayley rollback files. Distribution artifact: /home/trevor/docker/AirTrack/worktrees/logbook-v1-dist-20261127/artifacts/AirTrackSetup-1.1.3.exe.

- 2026-11-28 — Trevor approved the native 1.1.3 upgrade on Hayley. Matched installer fccc6af3df649b5827930cf6e024893a41e41eaa64df5467feb72b211986eeff from b9a4a9b / CI 46004365508 before launching Inno. Before 1.1.2, after 1.1.3; exit 0, transaction completed, database_ready. All 78 table counts and full data snapshot, config, and licence hashes match. Verified the installed Cockpit template, eight served assets and theme picker containing Default and Vintage Brass. No new browser visual pass, fresh install or Workshop/stable promotion. Rollback transaction on Hayley: C:/ProgramData/AirTrack/updates/backups/5e4fbb2a4e534396b0104106337aaafc. Protected verification in C:/Users/trevo/AirTrackTests/vintage-1.1.3-20261128.

- 2026-11-28 — Trevor explicitly asked to replace the Installer Workshop base. Atomically promoted native-qualified Windows 1.1.3 from b9a4a9b / CI 46004365508 to /home/trevor/docker/AirTrack/AirTrack-Windows/AirTrackSetup.exe. Verified 181483706 bytes and SHA-256 fccc6af3df649b5827930cf6e024893a41e41eaa64df5467feb72b211986eeff. Workshop status on :5500 and :5510 both reported the replacement. New customer ZIPs use this base. Existing Wombat ZIPs, stable feed and customer records were unchanged. No customer ZIP was generated or sent for this check. Recovery: atomically restore AirTrackSetup.exe.bak_pre_workshop_1.1.3_20261128 from the same directory, after verifying prior SHA-256 ba8bc68e447d5befb710e2af84a8789bd88a9a0e296f2238fd5244551a9b4aea, and recheck both Workshop status endpoints.

- 2026-11-28 — Windows 1.1.4 restore repair built from e273f92 in GitHub Actions 46106008690. Both artifact ZIP digests and packaged version/assets verified. Installer SHA-256 fde887d6eece5929344022523b13e256ad4096d362ee7a2f1c0715143f294f38, 181484003 bytes. Installed on Hayley with the guarded native upgrade from 1.1.3. Inno exit 0, transaction completed, version 1.1.4 and database ready. Before/after counts for 78 tables, SQL data snapshot and config/licence hashes match. Native MariaDB executable accepted a read-only SQL statement over stdin on configured port 3307. The Windows copy of airtrack_backup_20261128_120513.sql matches the server SHA-256 and was the newest completed SQL at verification. The source backup was not imported into Hayley. Protected rollback transaction: C:/ProgramData/AirTrack/updates/backups/39557c94393049beb073131aaf5e5841. Verification: C:/Users/trevo/AirTrackTests/restore-1.1.4-20261128. Candidate installer: /home/trevor/docker/AirTrack/worktrees/logbook-v1-dist-20261127/artifacts/AirTrackSetup-1.1.4.exe. Workshop and stable channel still use their existing artifacts.

- 2026-11-28 — Windows 1.1.5 candidate 82d0746 built in CI 46108877468; verified both artifact digests and bundled Home/ Airlines CSS. Installer SHA-256 362faaabfb40dd882d44d1eb41af8cbe0c9dd42bd367a0281f12738a9d26533f, 181486197 bytes. Native disposable Windows CI 46109202369 on qualification branch 815e4af passed fresh 1.1.5 and 1.1.4 to 1.1.5 upgrade. Both health checks passed and upgrade retained its database marker and config hash. Test used synthetic sidecars. Hayley received only the Airlines CSS and actual rendered markup replay passed. Isolated server dump restore reproduced MariaDB 1227 on australia_export due to server-specific DEFINER; see app.py journal. No installation on Hayley, publishing, Workshop replacement or database mutation. Candidate at /home/trevor/docker/AirTrack/worktrees/logbook-v1-dist-20261127/artifacts/AirTrackSetup-1.1.5.exe. Retain prior artifacts and Hayley recovery snapshot.
