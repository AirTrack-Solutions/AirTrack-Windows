# File History: tests/test_community_share_eligibility.py
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Synthetic regression coverage for pool download sharing suppression.

## Known Issues / Future Work
Does not replace native installer qualification.

## Entry Log
- 2026-11-23: Before creating test: exercise actual sharing functions with temporary images and isolated Flask/service mocks. Cover embedded provenance after rename, hash fallback and stale provenance, pool-only/mixed selectors, direct pool POST rejection, missing/path/symlink exclusions. No production photos, network or DB.

- Verification: same source functions tested with synthetic fixtures in native158/162 runtimes; Windows route source compiles and detail template parses. Installer not rebuilt/deployed for this change.

- Added positive mixed-gallery POST regression: original photo can still enqueue after per-photo confirmation, while pool images cannot.
