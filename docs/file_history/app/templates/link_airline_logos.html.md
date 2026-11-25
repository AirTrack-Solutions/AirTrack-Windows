# File History: app/templates/link_airline_logos.html
Journal Revision: 1
Last Updated: 2026-11-25

## Current State
Windows1.1.1 corrected candidate4911e1a is built, native-upgrade qualified and available as Workshopbase; stablefeed unchanged. Latest qualification below.
Existing Cockpit-linked page; journal begins with selected-theme integration.

## Known Issues / Future Work
Browser visual acceptance pending.

## Entry Log

- 2026-11-24 — Trevor reports HUD links opening old-colour pages. Ensure selected-theme assets/body hook for this local Cockpit page; scoped brass styles added. Existing forms/actions/content/security gates untouched. Jinja parse and live file hashes checked; browser visual acceptance pending. Windows source only. Recovery restore template from remote /home/airtrack/backups/hud-theme-pages-20261124 and regenerate prior CSS.

  Deployment verification:158 theme hooks PASS;162 host-owned templates required existing app-container write path, completed without replacing platform-specific content. Both CSS HTTP bytes match; graceful web reload done. Jinja parse PASS; visual review pending.

- 2026-11-25 final Windows qualification: source4911e1af7c97ca8e5cb0adf9372910d9047c3b32, CI45596368462 success. Corrected installer181475655bytes SHA256ba8bc68e447d5befb710e2af84a8789bd88a9a0e296f2238fd5244551a9b4aea; artifactZIPb2edd14fa7a0a7a9baf340a21adc5941e5f81218aee85a264f1af70cbe929bb5 verified. Hayley real Inno upgrade first1.1.0→1.1.1 then corrected same-version rebuild exits0/noOSreboot, native transactioncompleted. Full SQL data dump hash, all78table counts, licence/config hashes identical to original1.1.0;0aircraft/85581airports retained. Compiledserved active/securedart, vintageCSS, shutdownJS/themeLoader normalized hashes match source. Real picker endpoint regenerates correct packaged app/static:13themes includingVintage/default, generatedCSSimportsVintage. Service restart remains1.1.1/database_ready and13themes. User browser visual layout not separately exercised; images/settings/source already accepted live158/162. No virginOS/MSI-absent install, GUIwizard or1.0.5→1.1.1upgrade claim; actualfresh1.1.0qualification remains recorded separately. Qualified correctedcandidate nowWorkshopbase;5500/5510status181.5MBverified. Prior1.1.0 retained AirTrackSetup.exe.bak_pre_vintage_1.1.1_20261125 and originalcandidatefolder. First88476adartifactBLOCKED (wrongfrozenstaticroot), notdistributed. Native corrected recovery C:\ProgramData\AirTrack\updates\backups\bd8a1b3826194f109459098429430782; prior1.1.0transactionalso retained. Stable automaticfeed unchanged, no realcustomerpackage/email/purchase, SDverificationuntouched. Restore oldWorkshopbase only forfuturepackages; use native guardedtransaction forinstalledrollback, never overwrite lateruserdata blindly.
