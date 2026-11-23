# File History: app/utils/image_stats.py
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Windows candidate includes158 actual-file image counting and ground-exclusion statistics.

## Entry Log
- Before edit: port verified158 available linked-photo counter and fixed ground-exclusion SQL sources to Windows candidate. Retain native upload paths through current_app.static_folder. No customer data included.

- Port completed; three SQLite/filesystem regression tests PASS locally. Native CI includes same tests, permits Windows symlink restriction without dropping other assertions. Native installation qualification pending. Recovery revert scoped source commit; no data migrations.
