# File History: app/app.py
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Imported and registered the existing notam_bp alongside core blueprints. No optional-module scanner dependency; header already shows NOTAMs when endpoint exists.

Existing main app registers core blueprints but omits the database-backed NOTAM blueprint; /notams returned404 in actual frozen Windows test.

## Known Issues
NOTAM page unavailable in current Windows build.

## Future Work
Wire existing NOTAM page into V1 and verify on Hayley.

## Entry Log
- 2026-10-25: Created before change after actual Hayley test returned404; inspected main blueprint registration, real notam_routes.py and server template. No historical changes inferred.

- 2026-10-25: Imported and registered the existing notam_bp alongside core blueprints. No optional-module scanner dependency; header already shows NOTAMs when endpoint exists. Syntax check passes; rebuilt actual Windows smoke verification pending. Recovery: revert scoped blueprint additions/template. Existing database schema and live Hayley installation unaffected.
