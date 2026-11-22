# File History: app/utils/photo_backup.py
Journal Revision: 1
Last Updated: 2026-11-22

## Current State
Community feature installer candidate.

## Known Issues / Future Work
Retain signed updater and native service/database behavior; compiled qualification pending.

## Entry Log

- 2026-11-22 before edit: Trevor authorises community sharing/downloadableLogbook. Port qualified native client feature with defaults-off/local consent, metadata/credit retention, own-db matches and ATC review. Preserve Windows native service/updater/Weather hooks. Candidate release1.1.0; build artifact first, no stable feed switch until qualification.

- 2026-11-22 candidate source ready: default-off community settings/manual-sharing/own-DB reg+MSN+type+hex matching, fresh contributor approval gate, missing-only downloads, metadata and embedded credit/licence retention, portable local locks/private backup state. Explicit native source deltas retain updater/service/Weather. Twelve community and nine metadata tests pass in isolated153Python3.11/Pillow13 runtime (not a native Windows claim). Additional hidden imports and CI regressions added. Candidate1.1.0, stable feed/base installer remains1.0.5 until compiled qualification. Recover by reverting candidate source only; no Windows data changed.

- 2026-11-22 Windows CI portability correction:44983270821 revealed WinError32 replacing an open NamedTemporaryFile; close/fsync temporary JSON before atomic replacement. Backup blob handles also close before cleanup. No lock/consent policy relaxation. Native Windows test rerun required before release.

- 2026-11-22 native backup regression: Windows lock-file bytes cannot be read through another handle while held. Exclude only root automation.lock/preferences.lock from saved manifest; shared locks remain held across snapshot and ALL preferences/outbox/provenance/consent files remain included. Locks are regenerated on next operation, not user data. NativeCI44983746564caught this, no release published.
