---
title: Astrolabe · Runs · Legacy Rpi Migration · Reports · Coverage
version: 2
id: 7758f7e40448943bda3025d8271396c1
createdAt: 2026-09-17T11:58:30.276Z
updatedAt: 2026-09-17T11:58:30.276Z
---
> Imported from `.astrolabe/runs/legacy-rpi-migration/reports/coverage.md` on 2026-09-17. The original file remains in place.

---

# Acceptance coverage review
Inspected behavioral assertions in tests/test_migrate_rpi_project.py. AC1.1 core and schema parsed by Hypercube parser; AC1.2 raw SESSION bytes archived and indented history; AC1.3 guidance, plan and unknown bytes; AC2.1 preview no target; AC2.2 absent source, existing target and source symlink; AC2.3 injected copy failure leaves no target/stage; AC2.4 repeated CLI and API no-op. All criteria have automated assertions; no manual-only criterion.
