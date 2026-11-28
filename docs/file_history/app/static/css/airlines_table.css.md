# File History: app/static/css/airlines_table.css
Journal Revision: 1
Last Updated: 2026-11-28 Australia/Sydney

## Current State
At 768 CSS px and wider, the Windows Airlines table gives the Actions column more space and fits the four buttons on one row. Live Hayley deployment is pending.

Ported the signed-off Logbook V1 responsive and Vintage Brass release work to this target. See the V1 distribution journal for scope, verification and recovery.

## Entry Log
- 2026-11-27 — Included this file in the release integration scope from the signed-off .158 handoffs.

- 2026-11-28 — Trevor requested a single line for the Airlines row actions. Reallocated fixed table width to Actions, reduced the count column and let direct action buttons shrink within the cell. Delete confirmation and the narrow-screen layout retain their existing rules. Chromium fixtures with Bootstrap and Vintage Brass passed at 768, 1024, 1280 and 1858 px for button alignment, label fit and wide-logo containment. Hayley LAN and overlay SSH both timed out. Live deployment and browser confirmation pending. Revert these scoped CSS rules to recover.
