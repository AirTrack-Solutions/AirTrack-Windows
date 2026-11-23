# File History: gates/gate3/compile_installer.ps1
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Qualified 1.1.0 tester candidate is the Installer Workshop base. Fresh native Hayley installation and photo workflow passed; stable automatic-release feed remains 1.0.5. See final entry for exact artifact and limits.

## Known Issues / Future Work
Native build and fresh install qualification required.

## Entry Log
- Before edit: use app/windows_release.json as sole version source passed into Inno compiler, retain signed manifest checks and per-ref build isolation.

- 2026-11-23 candidate preparation: fresh bootstrap wired through checked Inno Exec, missing sidecars refused before install, old unchecked Run bootstrap/shared root constant removed. Fixed PowerShell reserved HOME variable collision and native argument arrays; actual Hayley Windows PowerShell AST parse passes. End-to-end installation qualification pending. Release uses one version manifest.

- 2026-11-23 final candidate qualification: source7043e7ea61df05419a707efb2464ae83387704df, successful CI45116801167. Exact installer175320364bytes SHA25671e22648bb956ad67755126c04ff716c34ff9e719e3757ba6ce6b2c7ea8c9d4d. Genuine Inno fresh application/database installation on Hayley, using existing MariaDB binaries and new instance, passed exit0, LocalSystem services, all8migrations, version1.1.0/database_ready. Deliberately invalid configuration returned exit1 and created no services. Native aircraft creation/photo upload/display and registration/MSNXMP passed. Sharing defaults off and no share link when opted out. Wombat publicHTTPS signed/hash-verified airport delivery imported85581rows and confirmed receipt. Original saved licence hash exactly retained; fixture removed, remainingaircraft0, restart remains healthy, automatic update task ready, DBloopbackonly. New Workshop base promoted; previous1.0.5base retained as AirTrackSetup.exe.bak_pre_tester_1.1.0_20261123. Stable automatic-release feed unchanged. No virgin Windows OS/MSI-absent installation, interactive wizard, full machine reboot or1.0.5->1.1.0upgrade acceptance claimed. No external tester package, email or real purchase generated. Further outside-user feedback remains necessary.
