# File History: gates/gate3/requirements.txt
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Windows installer dependencies are pinned here. pyOpenSSL is now pinned to 26.4.0, whose PyPI metadata requires cryptography>=49,<51 and accepts the existing 50.0.0 pin.

## Known Issues
Build run 40188562311 stopped in dependency resolution before compilation.

## Future Work
Verify the retried Windows installer build.

## Entry Log
- 2026-10-25: Created before repairing the build dependency conflict found while implementing V1 NOTAM airport choices. Existing requirements and failed build log read; no historical changes inferred.

- 2026-10-25: Updated only pyOpenSSL 26.3.0 -> 26.4.0 after verifying official PyPI JSON requires_dist metadata. Retained cryptography 50.0.0 rather than downgrade to satisfy the old pin. Recovery: revert this one-line change (which restores the known dependency conflict). Build verification pending.

- 2026-10-25: Build 40188688927 (775d782, branch codex/v1-notam-airports-20261025) passed and artifact installed as the Workshop base. Loader implementation commit fbe5c0b; dependency repair 775d782. Real Windows runtime remains untested. Recovery base and hashes recorded in docs/file_history/AirTrackSetup.exe.md.

- 2026-10-25: Hayley actual startup failed on ModuleNotFoundError mariadb imported by utils/export_mobile_db.py. Added mariadb==1.1.14; official PyPI metadata confirms cp312 win_amd64 wheel. Actual runtime evidence supersedes compile-only readiness. Rebuild pending.
