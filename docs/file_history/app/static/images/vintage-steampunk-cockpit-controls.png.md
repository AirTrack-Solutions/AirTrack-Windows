# File History: app/static/images/vintage-steampunk-cockpit-controls.png
Journal Revision: 1
Last Updated: 2026-11-25

## Current State
Windows1.1.1 corrected candidate4911e1a is built, native-upgrade qualified and available as Workshopbase; stablefeed unchanged. Latest qualification below.
Built-in image_gen edit adds vintage aircraft yoke and throttle to lower cockpit. Original image retained separately.

## Known Issues / Future Work
User browser visual acceptance pending; live gauge/HUD geometry unchanged.

## Entry Log
- 2026-11-24 — Trevor requests aircraft controls. Generated variant inspected and installed158/162; HTTP bytes match source. Windows source only. Recover by restoring CSS reference to original cockpit filename.

## Generation prompt (built-in image_gen)
Edit this cockpit background image with minimal strictly localized additions. Preserve EXACTLY the image composition, dimensions, framing, lighting, windscreen/hangar view, brass trim, left and right blank switch panels, report mounting plaque and entire wide blank central instrument shelf. This is a real application background with live controls positioned over it, so the top 65% of the image MUST remain unchanged. Add only in the bottom 35%: an authentic vintage aircraft control yoke on a slender brass column in front of the left seat (center around x29%, y81%), dark polished wooden grip with patinated brass hub, top of yoke below y69%; and a tasteful small brass throttle quadrant with three slender levers and black/ivory/red rounded knobs on the center leather console around x51%,y83%. Mechanically plausible aircraft controls, matching existing photorealistic worn leather/walnut/brass steampunk aesthetic. No added text, no new gauges, no people. Do not cover, shift or redraw any instrument mounting surfaces or side panels.


- 2026-11-25 final Windows qualification: source4911e1af7c97ca8e5cb0adf9372910d9047c3b32, CI45596368462 success. Corrected installer181475655bytes SHA256ba8bc68e447d5befb710e2af84a8789bd88a9a0e296f2238fd5244551a9b4aea; artifactZIPb2edd14fa7a0a7a9baf340a21adc5941e5f81218aee85a264f1af70cbe929bb5 verified. Hayley real Inno upgrade first1.1.0→1.1.1 then corrected same-version rebuild exits0/noOSreboot, native transactioncompleted. Full SQL data dump hash, all78table counts, licence/config hashes identical to original1.1.0;0aircraft/85581airports retained. Compiledserved active/securedart, vintageCSS, shutdownJS/themeLoader normalized hashes match source. Real picker endpoint regenerates correct packaged app/static:13themes includingVintage/default, generatedCSSimportsVintage. Service restart remains1.1.1/database_ready and13themes. User browser visual layout not separately exercised; images/settings/source already accepted live158/162. No virginOS/MSI-absent install, GUIwizard or1.0.5→1.1.1upgrade claim; actualfresh1.1.0qualification remains recorded separately. Qualified correctedcandidate nowWorkshopbase;5500/5510status181.5MBverified. Prior1.1.0 retained AirTrackSetup.exe.bak_pre_vintage_1.1.1_20261125 and originalcandidatefolder. First88476adartifactBLOCKED (wrongfrozenstaticroot), notdistributed. Native corrected recovery C:\ProgramData\AirTrack\updates\backups\bd8a1b3826194f109459098429430782; prior1.1.0transactionalso retained. Stable automaticfeed unchanged, no realcustomerpackage/email/purchase, SDverificationuntouched. Restore oldWorkshopbase only forfuturepackages; use native guardedtransaction forinstalledrollback, never overwrite lateruserdata blindly.
