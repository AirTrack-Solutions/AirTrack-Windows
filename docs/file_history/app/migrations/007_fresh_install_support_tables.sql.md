# File History: app/migrations/007_fresh_install_support_tables.sql
Journal Revision: 1
Last Updated: 2026-11-23

## Current State
Fresh schema repair in progress.

## Entry Log
- Before edit: genuinefreshHayleyuploadredirect500missingaircraft_manual_registry; canonical158schemaalsohasdisclaimer_acceptanceabsentWindowsbase. AddidempotentcanonicalCREATEIFNOTEXISTSvia migration forbothfreshandexistinginstalls. No rowdata copied.

- CanonicaltabledefinitionsaddedwithoutDROP/INSERT, so migrationpreservesexistingrecordsandcreatesemptytablesonlywhereabsent. Nativefixturetest/rebuiltfreshqualificationpending.
