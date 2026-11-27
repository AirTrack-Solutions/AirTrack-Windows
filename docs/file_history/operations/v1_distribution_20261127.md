# Logbook V1 distribution on AirTrack-Windows
Journal Revision: 1
Last Updated: 2026-11-27

## Current State

Hayley uses the original Vintage Brass button geometry and the shorter Windows Cockpit labels. The existing installer predates the label change.

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
