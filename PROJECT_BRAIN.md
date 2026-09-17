# Dental Clinic Management System (Nepal) — Project Memory

## Current State
- **Phase**: Phase 5 — Dental Chart (Odontogram) + Treatment Plans (Completed)
- **Status**: Added `clinical` app with FDI adult tooth charting (11-48), condition tracking (`CARIES`, `RCT`, `CROWN`), and Treatment Plans with NPR procedure costing.

## Architecture & Conventions
- **Framework**: Django 5.x
- **Timezone**: Asia/Kathmandu
- **Currency**: NPR (Nepali Rupee)
- **Patient ID**: Sequential per clinic (`generate_next_patient_id`).
- **Tooth Numbering**: Standard FDI Notation (11-48).

## Phase Map
- [x] Phase 0: Project Foundation
- [x] Phase 1: Multi-Tenant Foundation
- [x] Phase 2: Patients
- [x] Phase 3: Appointments + Queue
- [x] Phase 4: Clinical Encounters
- [x] Phase 5: Dental Chart + Treatment
- [ ] Phase 6: Finance + Patient Ledger
- [ ] Phase 7: Prescriptions
- [ ] Phase 8: Daily Business
- [ ] Phase 9: Patient Export + Documents
- [ ] Phase 10: Audit + Security Hardening
- [ ] Phase 11: Production / Commercial Hardening