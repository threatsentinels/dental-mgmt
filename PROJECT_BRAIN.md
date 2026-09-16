# Dental Clinic Management System (Nepal) — Project Memory

## Current State
- **Phase**: Phase 1 — Multi-Tenant Foundation (In Verification)
- **Status**: Added `tenants` (Clinic, Branch) and `accounts` (Custom User, UserRole) modules. Middleware attaches active tenant context to requests.

## Architecture & Conventions
- **Framework**: Django 5.x
- **Timezone**: Asia/Kathmandu
- **Currency**: NPR (Nepali Rupee)
- **Custom User Model**: `apps.accounts.User`
- **Tenant Context**: `request.clinic` and `request.branch` attached by `TenantMiddleware`.

## Phase Map
- [x] Phase 0: Project Foundation
- [x] Phase 1: Multi-Tenant Foundation
- [ ] Phase 2: Patients
- [ ] Phase 3: Appointments + Queue
- [ ] Phase 4: Clinical Encounters
- [ ] Phase 5: Dental Chart + Treatment
- [ ] Phase 6: Finance + Patient Ledger
- [ ] Phase 7: Prescriptions
- [ ] Phase 8: Daily Business
- [ ] Phase 9: Patient Export + Documents
- [ ] Phase 10: Audit + Security Hardening
- [ ] Phase 11: Production / Commercial Hardening