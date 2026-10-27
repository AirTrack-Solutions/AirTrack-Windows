# File History: docs/windows-updates.md
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
2026-10-27 candidate in progress: signed staging CLI plus independent SYSTEM daily/idle/on-AC task; seven-day postponement, pre-install hash recheck, existing transaction backups/rollback and interrupted-state recovery. Release identity1.0.2. Full Windows validation pending; no customer publication yet.

Operational instructions being written for V1 application updates; runtime acceptance remains pending.

## Entry Log
- 2026-10-26: Created before documenting the authorized updater, publishing and recovery workflow. No historic behavior inferred. See operations/windows_application_updates.md for validation record.

- 2026-10-27: Implemented automatic-update candidate at Trevor's explicit request. Frozen stage-update CLI exits before external task launches installer. SYSTEM task runs daily3am, catches up when idle10minutes/onAC/network available, never reboots; signed stable feed, seven-day postponement, failed-release hash quarantine. Existing data/backup gate preserved; Rollback can recover missing config after interrupted replacement. Existing installation location fix UsePreviousAppDir=no verified by successful isolated full installer1.0.1. Source tests before build: signature7, automatic policy4, routes3 passed in dependency environment. Pending full new-binary/native task validation and main170 rollout. Recovery disable task AirTrack-Update-<service>, use saved recover.ps1 and transaction state; never bypass gate.
