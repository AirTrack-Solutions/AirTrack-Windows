# File History: app/templates/metars.html
Journal Revision: 1
Last Updated: 2026-10-26

## Current State
Client METAR display/settings support pending. Existing source inspected before editing.

## Known Issues
Windows binary must be rebuilt and smoke tested.

## Future Work
Verify local weather station settings and METAR display on Hayley.

## Entry Log
- 2026-10-26: Created before porting Logbook158 METAR display/fixes into Windows V1. No past history inferred.

- 2026-10-26: Ported settings-backed METAR display, freshness/fallback/date/layout/name fixes from158 into client. Registered blueprint/menu and added Weather field to existing client Settings panel. Weather station saves validate/normalize codes, allow explicit clearing and preserve existing list if field omitted. NOTAM installer-only choices unchanged. Verification/rebuilt artifact pending. Recovery: revert this scoped commit; retain prior Workshop base until Windows smoke passes.
