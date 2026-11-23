# File History: gates/gate3/compile_installer.ps1
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Installer version consistency repair in progress.

## Known Issues / Future Work
Native build and fresh install qualification required.

## Entry Log
- Before edit: use app/windows_release.json as sole version source passed into Inno compiler, retain signed manifest checks and per-ref build isolation.

- 2026-11-23 candidate preparation: fresh bootstrap wired through checked Inno Exec, missing sidecars refused before install, old unchecked Run bootstrap/shared root constant removed. Fixed PowerShell reserved HOME variable collision and native argument arrays; actual Hayley Windows PowerShell AST parse passes. End-to-end installation qualification pending. Release uses one version manifest.
