# File History: gates/gate3/install_fresh.ps1
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Fresh native installer bootstrap repair in progress.

## Known Issues / Future Work
Native MariaDB/MSI/LocalSystem qualification required. Never overwrite an existing database as a fresh install.

## Entry Log
- Before implementation: replace unchecked Run steps/shared root password with checked bootstrap, unique per-install root secret, loopback DB, isolated new data directory, protected files, service/version/database health verification. Reuse installed MariaDB binaries safely if the AirTrackDB instance is absent. No Hayley removal until licence preserved and candidate ready. Official MariaDB install-db Windows service/datadir/port options reviewed.

- 2026-11-23 candidate preparation: fresh bootstrap wired through checked Inno Exec, missing sidecars refused before install, old unchecked Run bootstrap/shared root constant removed. Fixed PowerShell reserved HOME variable collision and native argument arrays; actual Hayley Windows PowerShell AST parse passes. End-to-end installation qualification pending. Release uses one version manifest.

- Nativefreshqualificationcaught32-bitInnoPowerShellProgramFilesredirection: existing64-bitMariaDBbinariesmissedandbootstrapfailed. Added64-bitinstallmodeandProgramW6432lookup. PostInstallRaiseExceptionloggedfailurebutInnoexit0; addedGetCustomSetupExitCodefresh/upgradefailureflag. Protectederror-summaryfileadded. Actualsamehelperrunin64-bitSSHcreatesDB/services; readinesspending. Earlierdefaultpathrefusalsafelyprotectedpre-existingJulytestfixtureC:\AirTrack(0-byteexe), usednewC:\AirTrackCandidateinstead, unrelatedfixtureretained. Fullcorrectedinstallerrebuild/retestrequired.

- NativeACLcheckcaughtinheritable-onlydirectoryflagsusedonregularcfg/licencefiles: icaclsreturned0butfileDACLempty, servicecouldnotreadconfig. ProtectnowusesplainFforfilesandOI/CIonlyfordirectories. Repairedonlycandidatecfg/licenceACLstoSYSTEM+AdminsF, restartedcandidateforfurtherdiagnosis. Fullfreshretestrequired.
