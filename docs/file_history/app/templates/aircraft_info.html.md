# File History: app/templates/aircraft_info.html
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Pool images are excluded from sharing controls; original photos remain available in mixed galleries.
Community feature installer candidate.

## Known Issues / Future Work
Retain signed updater and native service/database behavior; compiled qualification pending.

## Entry Log

- 2026-11-22 before edit: Trevor authorises community sharing/downloadableLogbook. Port qualified native client feature with defaults-off/local consent, metadata/credit retention, own-db matches and ATC review. Preserve Windows native service/updater/Weather hooks. Candidate release1.1.0; build artifact first, no stable feed switch until qualification.

- 2026-11-22 candidate source ready: default-off community settings/manual-sharing/own-DB reg+MSN+type+hex matching, fresh contributor approval gate, missing-only downloads, metadata and embedded credit/licence retention, portable local locks/private backup state. Explicit native source deltas retain updater/service/Weather. Twelve community and nine metadata tests pass in isolated153Python3.11/Pillow13 runtime (not a native Windows claim). Additional hidden imports and CI regressions added. Candidate1.1.0, stable feed/base installer remains1.0.5 until compiled qualification. Recover by reverting candidate source only; no Windows data changed.

- 2026-11-23: Trevor requests suppressing redundant sharing of pool downloads. Detect embedded PhotoID, with hash-matched local provenance fallback; exclude them from selector, hide aircraft sharing link when no eligible original exists, and redirect direct pool-only form requests back without queuing. Mixed galleries keep original photos selectable. Existing backend rejection and ownership/consent confirmation retained. No file/image/DB mutation or repository request during eligibility checks. Backup /home/trevor/docker/AirTrack/private/pool-share-ui-20261123/AirTrack-Windows. Verification follows.

- Verification: same source functions tested with synthetic fixtures in native158/162 runtimes; Windows route source compiles and detail template parses. Installer not rebuilt/deployed for this change.

- Added positive mixed-gallery POST regression: original photo can still enqueue after per-photo confirmation, while pool images cannot.
