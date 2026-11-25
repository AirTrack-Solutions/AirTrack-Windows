# File History: app/templates/admin_registries.html
Journal Revision: 1
Last Updated: 2026-11-24

## Current State
Existing Cockpit-linked page; journal begins with selected-theme integration.

## Known Issues / Future Work
Browser visual acceptance pending.

## Entry Log

- 2026-11-24 — Trevor reports HUD links opening old-colour pages. Ensure selected-theme assets/body hook for this local Cockpit page; scoped brass styles added. Existing forms/actions/content/security gates untouched. Jinja parse and live file hashes checked; browser visual acceptance pending. Windows source only. Recovery restore template from remote /home/airtrack/backups/hud-theme-pages-20261124 and regenerate prior CSS.

  Deployment verification:158 theme hooks PASS;162 host-owned templates required existing app-container write path, completed without replacing platform-specific content. Both CSS HTTP bytes match; graceful web reload done. Jinja parse PASS; visual review pending.
