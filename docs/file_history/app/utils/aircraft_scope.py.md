# File History: app/utils/aircraft_scope.py
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Qualified 1.1.0 tester candidate is the Installer Workshop base. Fresh native Hayley installation and photo workflow passed; stable automatic-release feed remains 1.0.5. See final entry for exact artifact and limits.

## Entry Log
- Before edit: port verified158 available linked-photo counter and fixed ground-exclusion SQL sources to Windows candidate. Retain native upload paths through current_app.static_folder. No customer data included.

- Port completed; three SQLite/filesystem regression tests PASS locally. Native CI includes same tests, permits Windows symlink restriction without dropping other assertions. Native installation qualification pending. Recovery revert scoped source commit; no data migrations.

- 2026-11-23 final candidate qualification: source7043e7ea61df05419a707efb2464ae83387704df, successful CI45116801167. Exact installer175320364bytes SHA25671e22648bb956ad67755126c04ff716c34ff9e719e3757ba6ce6b2c7ea8c9d4d. Genuine Inno fresh application/database installation on Hayley, using existing MariaDB binaries and new instance, passed exit0, LocalSystem services, all8migrations, version1.1.0/database_ready. Deliberately invalid configuration returned exit1 and created no services. Native aircraft creation/photo upload/display and registration/MSNXMP passed. Sharing defaults off and no share link when opted out. Wombat publicHTTPS signed/hash-verified airport delivery imported85581rows and confirmed receipt. Original saved licence hash exactly retained; fixture removed, remainingaircraft0, restart remains healthy, automatic update task ready, DBloopbackonly. New Workshop base promoted; previous1.0.5base retained as AirTrackSetup.exe.bak_pre_tester_1.1.0_20261123. Stable automatic-release feed unchanged. No virgin Windows OS/MSI-absent installation, interactive wizard, full machine reboot or1.0.5->1.1.0upgrade acceptance claimed. No external tester package, email or real purchase generated. Further outside-user feedback remains necessary.
