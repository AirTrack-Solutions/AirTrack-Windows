# Logbook V1 distribution on AirTrack-Windows
Journal Revision: 1
Last Updated: 2026-11-27

## Current State

Windows 1.1.2 was built from 5d4345c and is available as a distribution artifact. The .158 production
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
