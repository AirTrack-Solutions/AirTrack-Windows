# File History: app/templates/notams.html
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Added existing Logbook airport-card display and safety footer to Windows, with local jquery-3.7.1.min.js reference; omitted glossary link because Windows has no glossary endpoint. Uses notam_airports from runtime config, not a fixed card count.

Template absent from Windows source; existing database-backed route expects it.

## Known Issues
NOTAM page unavailable in current Windows build.

## Future Work
Wire existing NOTAM page into V1 and verify on Hayley.

## Entry Log
- 2026-10-25: Created before change after actual Hayley test returned404; inspected main blueprint registration, real notam_routes.py and server template. No historical changes inferred.

- 2026-10-25: Added existing Logbook airport-card display and safety footer to Windows, with local jquery-3.7.1.min.js reference; omitted glossary link because Windows has no glossary endpoint. Uses notam_airports from runtime config, not a fixed card count. Syntax check passes; rebuilt actual Windows smoke verification pending. Recovery: revert scoped blueprint additions/template. Existing database schema and live Hayley installation unaffected.
