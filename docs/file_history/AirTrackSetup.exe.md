# File History: AirTrackSetup.exe
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Workshop base is corrected build40190160286, source1e76b9798314a6bb2ddb67a58ca29ebb981a4921. Includes NOTAM choices, MariaDB connector, registered page/template and corrected license destination. The compiled application passed an isolated Windows smoke test on Hayley. Prior build40188688927 was withdrawn after real Windows startup failed.

## Known Issues
Rebuilt binary required for the new [notams] airports config loader. Real Windows installation verification is separate from successful compilation.

## Future Work
Run a real Windows fresh-install smoke test before distributing to customers.

## Entry Log
- 2026-10-25: Created before replacing the Workshop base installer for V1 NOTAM airport choices. Existing base and build workflow inspected; no past build history inferred.

- 2026-10-25: Windows build succeeded through dependency installation, PyInstaller, Inno Setup and artifact upload. Verified artifact archive SHA256 78fe7d6a92ec26408e0b90bffaf441e7e69714a80beb5f3fdaa151c88ab88050, exact single expected filename and PE MZ header. Atomically replaced base: 89231757 bytes, SHA256 c9470cc89672fdcdb8e82089001ce21e7cf75871b29f1ee48f85f23eb40c9d12. Both ATC endpoints detect 89.2 MB. Recovery copy: /home/trevor/docker/AirTrack/AirTrack-Windows/AirTrackSetup.exe.bak_pre_notam_airports_20261025. Previous base SHA256 b4a4c6c99d07f0eb52c40c1ee3136ffe817e5201dc4c605dc27a42260940ce89. Existing customer ZIPs unchanged. Windows installation/service startup not exercised on a real Windows host.

- 2026-10-25: Actual Hayley startup test exposed missing mariadb module. Restored original base from .bak_pre_notam_airports_20261025 atomically; failing candidate retained as AirTrackSetup.exe.failed_smoke_20261025. Do not distribute candidate until runtime check passes. Rebuild includes connector.

- 2026-10-25 corrected base: artifact12598095395; archive sha256:6c393f2f12e72a2e0b592e8309236ea68a77af33622989cac24b119cd30adc5f verified, single expected PE filename/header checked. Atomically installed 89491298 bytes, EXE SHA256 fa5c555d60061f103e28a8c7cadc99b8deb05320fc8a4dcf41fe67613ae26901. Original pre-NOTAM recovery base remains AirTrackSetup.exe.bak_pre_notam_airports_20261025. Withdrawn failing candidate retained as AirTrackSetup.exe.failed_smoke_20261025. Actual clean compiled Windows application from build40190160286 (source1e76b9798314a6bb2ddb67a58ca29ebb981a4921) passed on Hayley via SSH in debug mode against a private cloned database on127.0.0.1:33317. /notams returned200 with all six configured cards; YSWS and YMML API endpoints returned200/count0 (no notices in copied DB). Actual binary accepted six codes and rejected seven/duplicates. No pip overlays in final bundle. Original AirTrackClient service path/config preserved, source config SHA unchanged, original service and both existing DB services running after test, temporary DB/app stopped and port33317 closed. This is a compiled-app smoke test, not a full Inno wizard/fresh-install/LocalSystem service test.
