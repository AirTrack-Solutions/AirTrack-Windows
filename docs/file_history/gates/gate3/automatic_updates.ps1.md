# File History: gates/gate3/automatic_updates.ps1
Journal Revision: 1
Last Updated: 2026-10-27

## Current State
2026-10-27 candidate in progress: signed staging CLI plus independent SYSTEM daily/idle/on-AC task; seven-day postponement, pre-install hash recheck, existing transaction backups/rollback and interrupted-state recovery. Release identity1.0.2. Full Windows validation pending; no customer publication yet.

Implementation planned: Administrator-installed SYSTEM scheduled update runner, next-run recovery and daily schedule.

## Known Issues
Must validate compiled Windows path before customer publication.

## Future Work
Automated signature/policy tests and isolated Hayley runtime tests.

## Entry Log
- 2026-10-27: Created before implementation under Trevor's explicit automatic update authorization. Use existing signed installer feed and transaction guard; no trust bypass, private keys or credentials in clients. Recovery: remove scheduled task to disable automatic runs; preserve installer transaction snapshots.

- 2026-10-27: Implemented automatic-update candidate at Trevor's explicit request. Frozen stage-update CLI exits before external task launches installer. SYSTEM task runs daily3am, catches up when idle10minutes/onAC/network available, never reboots; signed stable feed, seven-day postponement, failed-release hash quarantine. Existing data/backup gate preserved; Rollback can recover missing config after interrupted replacement. Existing installation location fix UsePreviousAppDir=no verified by successful isolated full installer1.0.1. Source tests before build: signature7, automatic policy4, routes3 passed in dependency environment. Pending full new-binary/native task validation and main170 rollout. Recovery disable task AirTrack-Update-<service>, use saved recover.ps1 and transaction state; never bypass gate.

- 2026-10-27: Bind scheduled installation to signed manifest version via RELEASEVERSION preflight; reject mismatched installer before replacement. Explicit test feed override still uses bundled public-key verification; production registration uses stable feed. Native full1.0.1 installer success and failed-migration rollback verified on isolated test service. First build commits f9d3b8a/ced6ee6 (script required force-add due existing ignore rules). Final native installer will include these later script corrections; compiled Python source remains ced6ee6.
