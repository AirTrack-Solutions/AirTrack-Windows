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
