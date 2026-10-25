# File History: gates/gate3/service.py
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Windows service reads per-customer airtrack.cfg before importing Flask. The [notams] airports setting is validated and loaded into NOTAM_PRIMARY_AIRPORTS and NOTAM_HOME_ICAOS before importing Flask. Legacy configs retain original four airports.

## Known Issues
Existing compiled installers require rebuilding to include Python service changes.

## Future Work
Verify rebuilt installer on a real Windows installation.

## Entry Log
- 2026-10-25: Created before adding NOTAM configuration support; inspected _load_config and installer build workflow. No prior history inferred.

- 2026-10-25: Added V1 per-package NOTAM airport configuration at Trevor request. One to six distinct ASCII four-letter codes; malformed config fails explicitly; existing process environment overrides retained. Actual _load_config tested with generated sidecar configs for one and six airports; syntax passes. No real Windows runtime test yet. Compiled base requires rebuild. Recovery: revert the loader change or restore previous base installer; existing configs without [notams] continue to work.

- 2026-10-25: Build 40188688927 (775d782, branch codex/v1-notam-airports-20261025) passed and artifact installed as the Workshop base. Loader implementation commit fbe5c0b; dependency repair 775d782. Real Windows runtime remains untested. Recovery base and hashes recorded in docs/file_history/AirTrackSetup.exe.md.
