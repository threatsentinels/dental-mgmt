# Dental Clinic Management System (Nepal) — Project Memory

## Current State
- **Phase**: Phase 8 — Daily Business & Operational Reports Engine (Completed)
- **Status**: Added `reports` app with daily operational closing metrics, patient footfall count, production totals, collections by channel (Cash, eSewa, Khalti, Fonepay), and day-sheet views.

## Architecture & Conventions
- **Framework**: Django 5.x
- **Timezone**: Asia/Kathmandu
- **Currency**: NPR (Nepali Rupee)
- **Financial Architecture**: Decoupled Charges vs Payments with real-time daily closing summaries.

## Phase Map
- [x] Phase 0: Project Foundation
- [x] Phase 1: Multi-Tenant Foundation
- [x] Phase 2: Patients
- [x] Phase 3: Appointments + Queue
- [x] Phase 4: Clinical Encounters
- [x] Phase 5: Dental Chart + Treatment
- [x] Phase 6: Finance + Patient Ledger
- [x] Phase 7: Prescriptions
- [x] Phase 8: Daily Business
- [ ] Phase 9: Patient Export + Documents
- [ ] Phase 10: Audit + Security Hardening
- [ ] Phase 11: Production / Commercial Hardening