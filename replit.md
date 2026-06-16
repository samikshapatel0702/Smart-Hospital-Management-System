# Smart Hospital Management System

A console-based Python application to automate hospital operations — patient registration, doctor/nurse management, appointments, billing, pharmacy, lab reports, and medical records.

## Run & Operate

- `python3 -m hospital_management.main` — launch the interactive menu (from project root)
- Data is auto-saved to `hospital_management/data/*.json`
- CSV reports exported to `hospital_management/data/appointments_<date>.csv` and `billing_report_<date>.csv`
- Activity log written to `hospital_management/data/activity.log`

## Stack

- Python 3.11
- Standard library only: `abc`, `uuid`, `datetime`, `json`, `csv`, `os`
- pnpm workspaces (Node.js artifacts co-exist in the same repo)

## Where things live

- `hospital_management/models/` — all OOP classes (Person, Patient, Doctor, Nurse, Appointment, Bill, Medicine, MedicalRecord, LabReport, Hospital)
- `hospital_management/utils/decorators.py` — logging decorators for patient registration, appointment booking, bill generation
- `hospital_management/utils/file_handler.py` — JSON save/load + CSV export utilities
- `hospital_management/data/` — runtime data storage (JSON, CSV, log)
- `hospital_management/main.py` — full menu-driven console interface

## Architecture decisions

- `Person` is an ABC; `Patient`, `Doctor`, `Nurse` all inherit and override `display_details()` (polymorphism).
- `Hospital` class uses composition — owns all entity collections; no global state.
- All attributes are private (`__`); accessed via `@property` (encapsulation).
- Recursive patient search (`_recursive_search`), lambda sorts for doctors/medicines/appointments, generators for streaming lab reports and bills.
- `@log_patient_registration`, `@log_appointment_booking`, `@log_bill_generation` decorators write to `activity.log`.
- Data persisted as JSON (records) and CSV (daily reports).

## Product

Full-featured hospital management console app covering: Patient Management, Doctor Management, Nurse Management, Appointment Scheduling, Pharmacy, Medical Records, Lab Reports, Billing, CSV Report Generation, and Statistics.

## Gotchas

- When adding a doctor, enter just the name (e.g. `Chen`) — the display prepends `Dr.` automatically.
- Blood group input must be exact: `A+`, `A-`, `B+`, `B-`, `O+`, `O-`, `AB+`, `AB-`
- Nurse shift must be exactly: `Morning`, `Afternoon`, or `Night`
- Run from the repo root so relative imports resolve correctly.
