# File History: app/static/css/themes.css
Journal Revision: 1
Last Updated: 2026-11-28 Australia/Sydney

## Current State
Ported the signed-off Logbook V1 responsive and Vintage Brass release work to this target. See the V1 distribution journal for scope, verification and recovery.

## Entry Log
- 2026-11-27 — Included this file in the release integration scope from the signed-off .158 handoffs.

- 2026-11-28 — After Hayley reported no visible radar alignment change, found the served generated import still tagged the preceding Vintage Brass revision. Updated only its cache token to the deployed stylesheet modification time, 1795839839, and confirmed the import over HTTP. No service restart or database writes. Live browser confirmation remains pending. Recover the previous generated CSS from C:/Users/trevo/AirTrackTests/restore-1.1.4-20261128/themes-before-radar-cache.css.

- 2026-11-28 — Refreshed the generated Hayley Vintage Brass stylesheet import to 1795840502 for the Home header fix. Verified the imported stylesheet and served Home page in Chromium replay. Recover prior generated CSS from C:/Users/trevo/AirTrackTests/restore-1.1.4-20261128/themes-before-home-plaque.css.
