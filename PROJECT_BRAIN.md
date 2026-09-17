# Dental Clinic Management System (Nepal) — Project Memory

## Current State
- **Phase**: Phase 4 — Clinical Encounters (Completed)
- **Status**: Added `encounters` app with doctor workspace notes, vitals recording (BP, pulse, temp), diagnosis logging, and direct patient profile integration.

## Architecture & Conventions
- **Framework**: Django 5.x
- **Timezone**: Asia/Kathmandu
- **Currency**: NPR (Nepali Rupee)
- **Patient ID**: Sequential per clinic (`generate_next_patient_id`).
- **Queue Tokens**: Daily sequential integer per clinic.

## Phase Map
- [x] Phase 0: Project Foundation
- [x] Phase 1: Multi-Tenant Foundation
- [x] Phase 2: Patients
- [x] Phase 3: Appointments + Queue
- [x] Phase 4: Clinical Encounters
- [ ] Phase 5: Dental Chart + Treatment
- [ ] Phase 6: Finance + Patient Ledger
- [ ] Phase 7: Prescriptions
- [ ] Phase 8: Daily Business
- [ ] Phase 9: Patient Export + Documents
- [ ] Phase 10: Audit + Security Hardening
- [ ] Phase 11: Production / Commercial Hardening