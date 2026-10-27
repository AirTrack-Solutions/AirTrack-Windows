# Windows V1 application updates
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Released/deployed1.0.3 on2026-10-27. Main Hayley (.170) bootstrapped to2 and then genuinely upgraded2->3 by the SYSTEM updater from the signed stable feed; database/aircraft/config/settings preservation passed. Native1.0.3 final SHA256c25fd4c9a7bdf8965988a85c70e5bcfd1836dcc21b244f6b9855802e9ca373eb (171899113bytes), native source99007a7 with release data3e78ec2; unchanged Python code from verified build40429896630/ced6ee6. Daily3am task catches up idle/online/onAC, continues if unplugged, supports seven-day postponement, no Windows reboot. See operations/windows_application_updates.md for acceptance and recovery.



## Design
- Existing installations receive one bootstrap upgrade; new Workshop installers include automatic updates. No repeated manual download/install is required for future signed releases.
- A SYSTEM task executes a frozen signed-staging CLI, waits for that process to exit, then launches the verified silent installer independently of the application service. Daily3am, catch up idle10minutes/online/onAC; do not abort if charger removed; no reboot. Logbook page offers seven-day postponement/resume.
- Use existing Wombat Ed25519 public trust root and a separate signed manifest domain binding product/version/URL/hash/size/expiry. Recheck file hash before execution; bind native RELEASEVERSION; quarantine failed hashes. Private key remains on153.
- Resolve target from registered service and disable Inno previous-dir reuse. Stop app, protect SQL/software backups, preserve licence/config/user uploads/settings, verify exact runtime version/tables/migrations. Commit terminal checkpoint before opening request gate, and resume terminal cleanup without replaying old SQL over later user writes. Compatible external runner is staged before program replacement.
- Rejected service-launched interactive installers and unchecked template overlays: session0 prompts and frozen/native file locks require an independent scheduled runner and verified full installer.

## Known Issues
Fresh wizard/MariaDB bootstrap was not re-exercised; existing-service upgrade and LocalSystem execution were verified. Interruption tests simulate missing files/residual gate, not a physical power cut. Hardware failure, unrelated external DB writers or failure of restoration itself can require administrator recovery; never delete a nonterminal gate to bypass it. Legacy clients still require their first bootstrap upgrade. Signed feed expires2026-11-26; owner must publish/renew a validated release before then. Windows Authenticode is separate from manifest signing.

## Future Work
Run a separate fresh-install acceptance test in a disposable Windows environment. For each next software release, build/validate it, increment version and publish once to Wombat; customers' installed tasks perform delivery. Keep protected recovery artifacts until verified no longer needed. Source remains on codex/v1-notam-airports-20261025; default branch not merged by this operation.

## Entry Log
- 2026-10-26: Read setup.iss journal, installed source/Marmot, existing updater review and shared memory before editing. Rejected silent service-launched interactive installer (session0/UAC) and unfinished template-overlay updater (cannot replace frozen Python/native libraries reliably). Scope is user-approved Windows application releases, not unattended V2 updates.

- 2026-10-27: Reproduced native installer refusal with diagnostics. Actual guard error is target/service mismatch, not dump failure: Inno selects original main app directory while /SERVICENAME=AirTrackUpdateTest resolves test service. Disable previous installation directory reuse so registry-derived DefaultDirName applies. Existing fail-closed guard preserved; verify full installer on isolated service before main upgrade.

- 2026-10-27 acceptance before main deployment: full native1.0.2 upgrade preserved configuration/licence/uploads/weather/aircraft; SYSTEM scheduled task downloaded the real signed HTTPS candidate and installed silently with exit0/status installed. That task test used actual1.0.2 code with administrative test-only metadata1.0.1 to simulate a prior version; main metadata untouched. Postponement honored by actual frozen CLI. Full1.0.1 invalid-migration installer rollback removed new SQL table and restored files; new guard and actual SYSTEM recovery task restored missing config/executable with phase rolled_back, healthy1.0.2, task exit0. All tests use isolated5017/33317. Final native installer SHA256 d1548d1b93085b40c8ae823edeb1243a3c7126dfb21e833b6774fd28b94924b5,171896386bytes. Compiled Python40429896630/ced6ee6; native scripts883a558. Candidate signed with existing Wombat key, independently verified HTTPS envelope/hash. Proceeding to one bootstrap upgrade of main170 after per-aircraft/settings/file fingerprint capture, then stable publication/customer Workshop base. No unrelated DB/service changes.

- 2026-10-27 completion: Main170 genuine2->final3 SYSTEM update returned0/statusinstalled, health3/database_ready; original aircraft digest/count1,15settings and2files preserved. Production taskSYSTEM daily03:00+11:00, idle/network/AC-start true, stop-on-unplug false. Stable/candidate final artifact c25fd4c9...; Workshop base identical and both5500/5510 read it. All test/verification scheduled tasks removed, isolated services stopped/disabled, production app/AirTrackDB/MariaDB remain running. Snapshots/private verification records retained in C:\Users\trevo\AirTrackTests\notam-20261025 and production C:\ProgramData\AirTrack\updates. Initial combined test wait timed out; independently checked rollback files/health/new-table removal rather than asserting lost harness output. Source commits f9d3b8a,ced6ee6,883a558,3e78ec2,99007a7; journal finalization commit follows. No customer communications or licence provisioning.
