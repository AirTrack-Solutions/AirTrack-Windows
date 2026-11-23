# File History: app/routes/aircraft_routes.py
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Qualified 1.1.0 tester candidate is the Installer Workshop base. Fresh native Hayley installation and photo workflow passed; stable automatic-release feed remains 1.0.5. See final entry for exact artifact and limits.

## Known Issues / Future Work
Retain signed updater and native service/database behavior; compiled qualification pending.

## Entry Log

- 2026-11-22 before edit: Trevor authorises community sharing/downloadableLogbook. Port qualified native client feature with defaults-off/local consent, metadata/credit retention, own-db matches and ATC review. Preserve Windows native service/updater/Weather hooks. Candidate release1.1.0; build artifact first, no stable feed switch until qualification.

- 2026-11-22 candidate source ready: default-off community settings/manual-sharing/own-DB reg+MSN+type+hex matching, fresh contributor approval gate, missing-only downloads, metadata and embedded credit/licence retention, portable local locks/private backup state. Explicit native source deltas retain updater/service/Weather. Twelve community and nine metadata tests pass in isolated153Python3.11/Pillow13 runtime (not a native Windows claim). Additional hidden imports and CI regressions added. Candidate1.1.0, stable feed/base installer remains1.0.5 until compiled qualification. Recover by reverting candidate source only; no Windows data changed.

- Before2026-11-23nativeURLrepair: realuploadedJPEGsrenderedasuploads%5Caircraft%5CfilenameandHTTP404becauseos.path.joinusesWindowsbackslashes. UseforwardslashURLpathsforprimary/gallery/listimages, retainingOSfilesystemjoinsforactualdiskwrites. Nativefixturemetadata/downloadverificationrequired.

- 2026-11-23 final candidate qualification: source7043e7ea61df05419a707efb2464ae83387704df, successful CI45116801167. Exact installer175320364bytes SHA25671e22648bb956ad67755126c04ff716c34ff9e719e3757ba6ce6b2c7ea8c9d4d. Genuine Inno fresh application/database installation on Hayley, using existing MariaDB binaries and new instance, passed exit0, LocalSystem services, all8migrations, version1.1.0/database_ready. Deliberately invalid configuration returned exit1 and created no services. Native aircraft creation/photo upload/display and registration/MSNXMP passed. Sharing defaults off and no share link when opted out. Wombat publicHTTPS signed/hash-verified airport delivery imported85581rows and confirmed receipt. Original saved licence hash exactly retained; fixture removed, remainingaircraft0, restart remains healthy, automatic update task ready, DBloopbackonly. New Workshop base promoted; previous1.0.5base retained as AirTrackSetup.exe.bak_pre_tester_1.1.0_20261123. Stable automatic-release feed unchanged. No virgin Windows OS/MSI-absent installation, interactive wizard, full machine reboot or1.0.5->1.1.0upgrade acceptance claimed. No external tester package, email or real purchase generated. Further outside-user feedback remains necessary.
