# Dental Clinic Management System (Nepal) — Project Memory

## Current State
- **Phase**: Phase 6 — Finance & Patient Ledger Engine (Completed)
- **Status**: Added `billing` app with decoupled Charges (production) & Payments (collections) supporting Nepal payment methods (eSewa, Khalti, Fonepay, Cash).

## Architecture & Conventions
- **Framework**: Django 5.x
- **Timezone**: Asia/Kathmandu
- **Currency**: NPR (Nepali Rupee)
- **Financial Architecture**: Decoupled Charges vs Payments with real-time balance calculations.

## Phase Map
- [x] Phase 0: Project Foundation
- [x] Phase 1: Multi-Tenant Foundation
- [x] Phase 2: Patients
- [x] Phase 3: Appointments + Queue
- [x] Phase 4: Clinical Encounters
- [x] Phase 5: Dental Chart + Treatment
- [x] Phase 6: Finance + Patient Ledger
- [ ] Phase 7: Prescriptions
- [ ] Phase 8: Daily Business
- [ ] Phase 9: Patient Export + Documents
- [ ] Phase 10: Audit + Security Hardening
- [ ] Phase 11: Production / Commercial Hardening