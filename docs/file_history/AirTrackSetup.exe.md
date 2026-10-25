# File History: AirTrackSetup.exe
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Workshop base Windows installer is build 40188688927 at source 775d7829a77df7617346724571492621eedb1393 and includes configurable NOTAM airports. It is bundled into new customer packages by ATC.

## Known Issues
Rebuilt binary required for the new [notams] airports config loader. Real Windows installation verification is separate from successful compilation.

## Future Work
Run a real Windows fresh-install smoke test before distributing to customers.

## Entry Log
- 2026-10-25: Created before replacing the Workshop base installer for V1 NOTAM airport choices. Existing base and build workflow inspected; no past build history inferred.

- 2026-10-25: Windows build succeeded through dependency installation, PyInstaller, Inno Setup and artifact upload. Verified artifact archive SHA256 78fe7d6a92ec26408e0b90bffaf441e7e69714a80beb5f3fdaa151c88ab88050, exact single expected filename and PE MZ header. Atomically replaced base: 89231757 bytes, SHA256 c9470cc89672fdcdb8e82089001ce21e7cf75871b29f1ee48f85f23eb40c9d12. Both ATC endpoints detect 89.2 MB. Recovery copy: /home/trevor/docker/AirTrack/AirTrack-Windows/AirTrackSetup.exe.bak_pre_notam_airports_20261025. Previous base SHA256 b4a4c6c99d07f0eb52c40c1ee3136ffe817e5201dc4c605dc27a42260940ce89. Existing customer ZIPs unchanged. Windows installation/service startup not exercised on a real Windows host.

- 2026-10-25: Actual Hayley startup test exposed missing mariadb module. Restored original base from .bak_pre_notam_airports_20261025 atomically; failing candidate retained as AirTrackSetup.exe.failed_smoke_20261025. Do not distribute candidate until runtime check passes. Rebuild includes connector.
