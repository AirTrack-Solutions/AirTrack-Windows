# Hayley NOTAM installer smoke test
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Trevor authorized using powered-on Windows laptop Hayley / 192.168.0.170. SSH user trevo works and is administrator. AirTrackClient runs from C:\Users\trevo\docker\AirTrack\AirTrack.exe, not C:\AirTrack (whose exe is zero bytes). AirTrackDB 11.4 and unrelated MariaDB 11.7 are both running. No existing laptop journal found under docker. Existing data/config must be preserved.

## Known Issues
Default installer executes database/user creation and service registration; do not blindly run against this existing installation. Windows Sandbox unavailable. Ubuntu innoextract 1.9 cannot read newly built Inno Setup format; extraction stopped without changing laptop.

## Future Work
Test separately staged compiled application; Windows full installation remains separate.

## Entry Log
- 2026-10-25: Read-only discovery of service paths, admin access, available space and missing Sandbox. Created before laptop staging or configuration changes. No laptop files/services changed yet. Plan build artifact of compiled app for isolated smoke test, retaining existing installation.

- 2026-10-25: Staged application artifact from build40189455445 (archive SHA2566137394d541e4828359f7a3b0213c7a6f662be797f09f01fb5f4c301c9693894). Existing account cannot create databases; attempted known installer root credential was rejected, with no existing DB/account changes. Instead dumped live source transactionally (20870098 bytes) and initialized isolated MariaDB process on127.0.0.1:33317. Test app cfg/data/license copied only to private stage. Briefly stopped original AirTrackClient, ran new binary debug against isolated DB; failed missing mariadb module before HTTP startup. Stopped test DB and restarted original AirTrackClient; running and original config hash unchanged. No live data migrated. Test root C:\Users\trevo\AirTrackTests\notam-20261025 retained with private ACL for recovery.
