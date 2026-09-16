# Dental Clinic Management System (Nepal) — Project Memory

## Current State
- **Phase**: Phase 2 — Patients (In Verification)
- **Status**: Built `Patient` model, registration form, medical alert safety indicators, patient search engine, and Patient Workspace foundation.

## Architecture & Conventions
- **Framework**: Django 5.x
- **Timezone**: Asia/Kathmandu
- **Currency**: NPR (Nepali Rupee)
- **Tenant Context**: Scope patient records via `request.clinic`.
- **Patient Identifier**: Unique per clinic scope (`P-00001`).

## Phase Map
- [x] Phase 0: Project Foundation
- [x] Phase 1: Multi-Tenant Foundation
- [x] Phase 2: Patients
- [ ] Phase 3: Appointments + Queue
- [ ] Phase 4: Clinical Encounters
- [ ] Phase 5: Dental Chart + Treatment
- [ ] Phase 6: Finance + Patient Ledger
- [ ] Phase 7: Prescriptions
- [ ] Phase 8: Daily Business
- [ ] Phase 9: Patient Export + Documents
- [ ] Phase 10: Audit + Security Hardening
- [ ] Phase 11: Production / Commercial Hardening