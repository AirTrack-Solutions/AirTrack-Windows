# File History: app/static/js/cockpit_shutdown.js
Journal Revision: 1
Last Updated: 2026-11-24

## Current State
Existing hidden switch sequence now has Vintage Brass presentation; this journal starts with this change.

## Known Issues / Future Work
Browser visual acceptance pending.

## Entry Log

- 2026-11-24 — Trevor approves visible moving brass toggles. Vintage-only eight keyboard buttons L1–L4/R1–R4 at lower panel lip, CSS lever positions mirror existing bank/progress storage. Existing1→4 shutdown/4→1 wake timers, wrong-order/bank rejection and hangar sequence retained. Other themes keep hidden div click zones/coordinates. Restore synchronizes visual/aria state. Verification recorded below; Windows source only. Recovery restore backed-up JS/CSS in /home/airtrack/backups/brass-switches-20261124 and regenerate themes; retain browser stored switch state.

  Verification: Node syntax PASS; isolated DOM/state-machine regression PASS for wrong-order/wrong-bank rejection, pressed lever state, complete shutdown/wake timers, legacy32px hidden target. Live158/162 JS/CSS exact HTTP bytes PASS. User browser visual acceptance pending; no real report/OS shutdown triggered.

- 2026-11-24 — Trevor requests instruments/HUD visible in secured state and toggle banks centred above respective gauge banks. Vintage stage4/secured overrides keep gauges/HUD/report visible/clickable above hangar layer(z2); existing stages2/3 dimming retained. Switches move to y44.7%, x25..35.5% and63..73.5%, centred on gauge-bank centres (~30.25/68.25%). Handlers/state/timing unchanged, legacy themes untouched. Node state regression/syntax PASS; live158162 JS/CSS exact-byte checks PASS, browser acceptance pending. Windows source only. Recovery remove final visibility CSS and restore prior switch coordinates.

- 2026-11-24 — Trevor rejects horizontal switch banks above gauges; requests2x2 at each panel end. Vintage-only targets now left x11/14%, right86.5/89.5%, rows48/56%; sequence1/2 top,3/4 bottom. Gauges/HUD/secured visibility/state logic unchanged. Node syntax/state regression PASS and live158/162 JS exact-byte check PASS; user visual acceptance pending. Windows source only. Recovery revert vintage positionZone coordinate block.

- 2026-11-24 — Trevor marks lower central panel screw as alignment axis. Vintage panel centre50.2% viewport: callsign on axis; gauge face centres at symmetric±11/17/23/29percentage-point offsets with half-width compensation; switch2x2 bank centres symmetric±37.7points. Keep vertical positions and HUD outside panel unchanged. Node syntax/state regression and live158/162 exact HTTP bytes PASS; user visual acceptance pending. Windows source only. Recovery remove final symmetry CSS and restore switch x expression.

- 2026-11-24 — Trevor marks unequal plaque gaps, approves left gauges unchanged, requests right mirrored and switch blocks centred in end spaces. Right gauge positions subtract61px outer diameter to correct observed screenshot offset; left untouched. Switch centres derive from actual outer gauge bounding edges and artwork panel ends8%/92%, keeping2x2 layout. Node syntax/state regression PASS; live158/162 exact HTTP JS/CSS bytes PASS, visual acceptance pending. Windows source only. Recovery remove last right-gap CSS and restore prior switchx calculation.
