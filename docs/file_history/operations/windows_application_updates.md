# Windows V1 application updates
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
Trevor authorized implementing user-approved V1 application updates while Claude is unavailable. Current Windows source can update capability/registry data but has no complete application updater. Existing drafts have unresolved signature/version, rollback and Windows file-lock issues and are not reused as trusted installed code.

## Design
- User checks for a release in Logbook, downloads a verified Windows installer, then explicitly runs it and approves Windows elevation. No session-0 interactive installer launch from the service.
- Reuse Wombat release hosting and its existing Ed25519 trust root, with a domain-separated signed manifest binding product/version/hash/size/URL/expiry. Never distribute private signing keys.
- Existing installations must be detected from service registration, stopped before replacement, and backed up. Preserve local config/license/user data; avoid database bootstrap on upgrades. Test failure and recovery before broad publication.
- New updater baseline requires one bootstrap upgrade for old clients; no assertion that old executables already contain it.

## Known Issues
Existing installer assumes C:\AirTrack, initializes DB on every run, and does not safely upgrade a running service. Full installer wizard/service-mode test has not yet run. Hayley original app/data must remain protected by isolated test fixtures first.

## Future Work
1. Signed release verification/download and user-facing check page with tests.
2. Upgrade-aware installer guard, backup/recovery and explicit compatibility handling.
3. Wombat release hosting/signing path without changing existing app-update protocol.
4. Build and isolated Hayley upgrade/failure tests, then a reviewed usable baseline.

## Entry Log
- 2026-10-26: Read setup.iss journal, installed source/Marmot, existing updater review and shared memory before editing. Rejected silent service-launched interactive installer (session0/UAC) and unfinished template-overlay updater (cannot replace frozen Python/native libraries reliably). Scope is user-approved Windows application releases, not unattended V2 updates.

- 2026-10-27: Reproduced native installer refusal with diagnostics. Actual guard error is target/service mismatch, not dump failure: Inno selects original main app directory while /SERVICENAME=AirTrackUpdateTest resolves test service. Disable previous installation directory reuse so registry-derived DefaultDirName applies. Existing fail-closed guard preserved; verify full installer on isolated service before main upgrade.
