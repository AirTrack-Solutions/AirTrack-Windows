# File History: gates/gate3/setup.iss
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Installer copies the customer license sidecar into _internal/config, creating that directory first, matching the actual frozen config.license runtime path.

## Known Issues
Actual Windows debug startup logged missing license until the sidecar was copied to the path named in that log. Existing customer license edition semantics are separate and unchanged.

## Future Work
Copy license into actual frozen config path and verify rebuilt artifact.

## Entry Log
- 2026-10-25: Created before correcting the license destination found during authorized Hayley smoke testing. Read installer and app/config/license.py; debug log establishes runtime path. Existing laptop installation not overwritten.

- 2026-10-25: Corrected only the license destination and ensured parent directory creation. In the separately staged test app, copying the existing license to this path changed the runtime result from missing-license fallback to successfully loaded license. No license re-signing or edition changes. Recovery: revert this scoped change. Inno compile verification pending.
