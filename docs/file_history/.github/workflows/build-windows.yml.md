# File History: .github/workflows/build-windows.yml
Journal Revision: 1
Last Updated: 2026-10-25

## Current State
Windows workflow compiles PyInstaller application and Inno Setup installer, uploads installer and a separate AirTrack-application bundle (14-day retention).

## Known Issues
Installer cannot be extracted by available innoextract version, and running it on Hayley would affect the existing service/database.

## Future Work
Validate artifact and isolated Windows startup.

## Entry Log
- 2026-10-25: Created before adding compiled-app artifact. Existing workflow read; no historical changes inferred.

- 2026-10-25: Added compiled application artifact without credentials/config/license sidecars, allowing smoke testing away from existing installations. Installer build/release steps unchanged. Recovery: remove added upload step. Workflow dispatched on feature branch; verification pending.

- 2026-10-25: Added --collect-all mariadb to carry connector package/native dependencies into frozen app after actual Windows smoke test exposed missing import. Application-artifact build40189455445 had succeeded but runtime failed. Rebuild pending.
