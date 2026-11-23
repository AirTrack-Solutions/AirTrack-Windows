# File History: app/config/license.py
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Before repair: mixed-case entitlement tables and lowercase constructor cause paid licences to fall back to Lite.

## Known Issues / Future Work
Keep legacy codes and existing entitlement counts.

## Entry Log
- 2026-11-23 before edit: audited and reproduced paid-edition fallback. Normalize table keys and inputs; no licence re-signing or permission expansion beyond purchased tier.

- 2026-11-23 normalized edition lookup maps and supplied edition with casefold, preserving ATP Personal2/ATF Professional10. Native candidate regression/build pending.
