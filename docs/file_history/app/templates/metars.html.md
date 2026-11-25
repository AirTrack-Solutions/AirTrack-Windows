# File History: app/templates/metars.html
Journal Revision: 1
Last Updated: 2026-11-25

## Current State
Windows1.1.1 corrected candidate4911e1a is built, native-upgrade qualified and available as Workshopbase; stablefeed unchanged. Latest qualification below.
Vintage Brass page-specific styling completed, including antique Cockpit instruments in existing positions. Standalone weather/Rabbit/Kiosk guide now load selected theme.
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

- 2026-11-24 — Address remaining teal on Add Airline, report/airport panels, weather, NOTAMs and utility pages. Add theme assets/body class to standalone pages; preserve existing functionality and non-vintage themes. NOTAM report uses block layout to prevent flex overflow and readable parchment text; operational severity indicators retained. Cockpit controls/brass-rim parchment gauges keep existing positions and animation, no background image. Verification and live deployment recorded below. Recovery: restore scoped files from vintage-refinement-20261124 backup and regenerate theme CSS; no data/settings changes. Windows source only, no installer rebuild.

  Verification: theme-generator regression/Python syntax PASS; live158/162 served stylesheet SHA256 matches source after regeneration/reload. Browser visual acceptance remains Trevor review. Client/Windows missing server-only files preserved; no installer rebuild. Recovery scoped backups /home/airtrack/backups/vintage-refinement-20261124.

- 2026-11-25 final Windows qualification: source4911e1af7c97ca8e5cb0adf9372910d9047c3b32, CI45596368462 success. Corrected installer181475655bytes SHA256ba8bc68e447d5befb710e2af84a8789bd88a9a0e296f2238fd5244551a9b4aea; artifactZIPb2edd14fa7a0a7a9baf340a21adc5941e5f81218aee85a264f1af70cbe929bb5 verified. Hayley real Inno upgrade first1.1.0→1.1.1 then corrected same-version rebuild exits0/noOSreboot, native transactioncompleted. Full SQL data dump hash, all78table counts, licence/config hashes identical to original1.1.0;0aircraft/85581airports retained. Compiledserved active/securedart, vintageCSS, shutdownJS/themeLoader normalized hashes match source. Real picker endpoint regenerates correct packaged app/static:13themes includingVintage/default, generatedCSSimportsVintage. Service restart remains1.1.1/database_ready and13themes. User browser visual layout not separately exercised; images/settings/source already accepted live158/162. No virginOS/MSI-absent install, GUIwizard or1.0.5→1.1.1upgrade claim; actualfresh1.1.0qualification remains recorded separately. Qualified correctedcandidate nowWorkshopbase;5500/5510status181.5MBverified. Prior1.1.0 retained AirTrackSetup.exe.bak_pre_vintage_1.1.1_20261125 and originalcandidatefolder. First88476adartifactBLOCKED (wrongfrozenstaticroot), notdistributed. Native corrected recovery C:\ProgramData\AirTrack\updates\backups\bd8a1b3826194f109459098429430782; prior1.1.0transactionalso retained. Stable automaticfeed unchanged, no realcustomerpackage/email/purchase, SDverificationuntouched. Restore oldWorkshopbase only forfuturepackages; use native guardedtransaction forinstalledrollback, never overwrite lateruserdata blindly.
