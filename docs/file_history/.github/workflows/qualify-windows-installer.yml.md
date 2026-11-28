# File History: .github/workflows/qualify-windows-installer.yml
Journal Revision: 1
Last Updated: 2026-11-28 Australia/Sydney

## Current State
Candidate-only disposable Windows qualification covers the 1.1.5 fresh installation and upgrade from 1.1.4.

## Entry Log
- 2026-11-28 — Added a branch-scoped native Windows matrix because Hayley has an existing database and is unsuitable for a clean install. Exercises the actual Inno artifacts, service/database readiness, upgrade row and configuration preservation, and served layout rules. Uses disposable configuration and licence fixture. Workflow results pending. Revert the candidate-only workflow to remove this qualification.

- 2026-11-28 — Adapted the branch-scoped fixture to 1.1.6. Fresh runner uses real Cockpit POSTs with session CSRF to check native backup pair, fail-before-write for a foreign SQL fixture, and successful local SQL restore. Separate runner checks 1.1.5 upgrade. Results pending.
