# File History: app/static/css/airlines_table.css
Journal Revision: 1
Last Updated: 2026-11-28 Australia/Sydney

## Current State
At 768 CSS px and wider, the Windows Airlines table gives the Actions column more space and fits the four buttons on one row. The updated stylesheet is deployed on Hayley.

Ported the signed-off Logbook V1 responsive and Vintage Brass release work to this target. See the V1 distribution journal for scope, verification and recovery.

## Entry Log
- 2026-11-27 — Included this file in the release integration scope from the signed-off .158 handoffs.

- 2026-11-28 — Trevor requested a single line for the Airlines row actions. Reallocated fixed table width to Actions, reduced the count column and let direct action buttons shrink within the cell. Delete confirmation and the narrow-screen layout retain their existing rules. Chromium fixtures with Bootstrap and Vintage Brass passed at 768, 1024, 1280 and 1858 px for button alignment, label fit and wide-logo containment. Hayley LAN and overlay SSH both timed out. Live deployment and browser confirmation pending. Revert these scoped CSS rules to recover.

- 2026-11-28 — Guarded Hayley stylesheet replacement served SHA-256 db73624aa28f136709f270ea10dde935091c93456acd9d8059721f2dada9f99e. Chromium replay of actual /airlines/ markup and styles showed all four controls aligned at 768, 1280 and 1858 CSS px. Restore C:/Users/trevo/AirTrackTests/restore-1.1.4-20261128/airlines-before-single-line.css to roll back. Also verified this stylesheet and the centred Home plaque are in Windows 1.1.5 artifact.
