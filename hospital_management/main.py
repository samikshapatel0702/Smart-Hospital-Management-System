"""
Smart Hospital Management System
Entry point — menu-driven console interface.
"""

import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hospital_management.models.hospital import Hospital


# ─── Helper I/O ──────────────────────────────────────────────────────────────

def _input(prompt: str) -> str:
    return input(f"  {prompt}").strip()


def _print_header(title: str) -> None:
    print(f"\n{'='*55}")
    print(f"  {title.upper()}")
    print(f"{'='*55}")


def _pause() -> None:
    input("\n  Press Enter to continue...")


# ─── Sub-menus ────────────────────────────────────────────────────────────────

def menu_patient_management(hospital: Hospital) -> None:
    while True:
        _print_header("Patient Management")
        print("  1. Register New Patient")
        print("  2. Update Patient Details")
        print("  3. Search Patient")
        print("  4. View Patient Medical History")
        print("  5. List All Patients")
        print("  6. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                name = _input("Name: ")
                age = int(_input("Age: "))
                gender = _input("Gender (M/F/Other): ")
                phone = _input("Phone: ")
                blood_group = _input("Blood Group (A+/A-/B+/B-/O+/O-/AB+/AB-): ")
                patient = hospital.register_patient(name, age, gender, phone, blood_group)
                patient.display_details()
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            try:
                pid = _input("Patient ID: ")
                field = _input("Field to update (name/age/gender/phone/blood_group): ")
                value = _input("New value: ")
                if field == "age":
                    value = int(value)
                hospital.update_patient(pid, **{field: value})
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "3":
            query = _input("Enter name/ID/phone to search: ")
            results = hospital.search_patient(query)
            if results:
                print(f"\n  Found {len(results)} result(s):")
                for p in results:
                    p.display_details()
            else:
                print("  No patients found matching that query.")

        elif choice == "4":
            try:
                pid = _input("Patient ID: ")
                patients = hospital.patients
                if pid not in patients:
                    print(f"  ERROR: Invalid Patient ID: {pid}")
                else:
                    patients[pid].view_records()
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "5":
            patients = hospital.patients
            if not patients:
                print("  No patients registered yet.")
            else:
                # List comprehension: active patients
                active = hospital.get_active_patients()
                active_ids = {p.patient_id for p in active}
                print(f"\n  Total patients: {len(patients)}")
                print(f"  Active (with scheduled appointments): {len(active)}\n")
                for p in patients.values():
                    tag = " [ACTIVE]" if p.patient_id in active_ids else ""
                    print(f"  • {p}{tag}")

        elif choice == "6":
            break
        else:
            print("  Invalid choice. Please try again.")
        _pause()


def menu_doctor_management(hospital: Hospital) -> None:
    while True:
        _print_header("Doctor Management")
        print("  1. Add Doctor")
        print("  2. Update Doctor Information")
        print("  3. Add Consultation Slot")
        print("  4. Remove Consultation Slot")
        print("  5. View Doctor Schedule")
        print("  6. List All Doctors (sorted by fee)")
        print("  7. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                name = _input("Name: ")
                age = int(_input("Age: "))
                gender = _input("Gender (M/F/Other): ")
                phone = _input("Phone: ")
                spec = _input("Specialization: ")
                fee = float(_input("Consultation Fee ($): "))
                doctor = hospital.add_doctor(name, age, gender, phone, spec, fee)
                doctor.display_details()
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            try:
                did = _input("Doctor ID: ")
                field = _input("Field to update (name/age/specialization/consultation_fee): ")
                value = _input("New value: ")
                if field == "age":
                    value = int(value)
                elif field == "consultation_fee":
                    value = float(value)
                hospital.update_doctor(did, **{field: value})
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "3":
            try:
                did = _input("Doctor ID: ")
                doctors = hospital.doctors
                if did not in doctors:
                    print(f"  ERROR: Invalid Doctor ID.")
                else:
                    date = _input("Date (YYYY-MM-DD): ")
                    time = _input("Time (HH:MM): ")
                    doctors[did].add_slot(date, time)
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "4":
            try:
                did = _input("Doctor ID: ")
                doctors = hospital.doctors
                if did not in doctors:
                    print(f"  ERROR: Invalid Doctor ID.")
                else:
                    date = _input("Date (YYYY-MM-DD): ")
                    time = _input("Time (HH:MM): ")
                    doctors[did].remove_slot(date, time)
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "5":
            did = _input("Doctor ID: ")
            doctors = hospital.doctors
            if did not in doctors:
                print("  ERROR: Invalid Doctor ID.")
            else:
                doctors[did].view_schedule()

        elif choice == "6":
            # Lambda: sort by fee
            sorted_docs = hospital.get_doctors_sorted_by_fee()
            if not sorted_docs:
                print("  No doctors registered yet.")
            else:
                print(f"\n  Doctors sorted by consultation fee (ascending):\n")
                for i, d in enumerate(sorted_docs, 1):
                    print(f"  {i:>3}. {d}")

        elif choice == "7":
            break
        else:
            print("  Invalid choice.")
        _pause()


def menu_nurse_management(hospital: Hospital) -> None:
    while True:
        _print_header("Nurse Management")
        print("  1. Add Nurse")
        print("  2. Assign Nurse to Patient")
        print("  3. Update Nurse Shift")
        print("  4. List All Nurses")
        print("  5. View Shift Policy")
        print("  6. Nurse Count by Shift")
        print("  7. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                name = _input("Name: ")
                age = int(_input("Age: "))
                gender = _input("Gender (M/F/Other): ")
                phone = _input("Phone: ")
                dept = _input("Department: ")
                shift = _input("Shift (Morning/Afternoon/Night): ")
                nurse = hospital.add_nurse(name, age, gender, phone, dept, shift)
                nurse.display_details()
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            try:
                nid = _input("Nurse ID: ")
                nurses = hospital.nurses
                if nid not in nurses:
                    print("  ERROR: Invalid Nurse ID.")
                else:
                    pid = _input("Patient ID to assign: ")
                    nurses[nid].assign_patient(pid)
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "3":
            try:
                nid = _input("Nurse ID: ")
                nurses = hospital.nurses
                if nid not in nurses:
                    print("  ERROR: Invalid Nurse ID.")
                else:
                    shift = _input("New Shift (Morning/Afternoon/Night): ")
                    nurses[nid].update_shift(shift)
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "4":
            nurses = hospital.nurses
            if not nurses:
                print("  No nurses registered yet.")
            else:
                print(f"\n  Total nurses: {len(nurses)}\n")
                for n in nurses.values():
                    print(f"  • {n}")

        elif choice == "5":
            from hospital_management.models.nurse import Nurse
            print(f"\n  {Nurse.hospital_shift_policy()}")

        elif choice == "6":
            from hospital_management.models.nurse import Nurse
            nurses_list = list(hospital.nurses.values())
            for shift in Nurse.VALID_SHIFTS:
                count = Nurse.count_by_shift(nurses_list, shift)
                print(f"  {shift} shift: {count} nurse(s)")

        elif choice == "7":
            break
        else:
            print("  Invalid choice.")
        _pause()


def menu_appointment_management(hospital: Hospital) -> None:
    while True:
        _print_header("Appointment Management")
        print("  1. Book Appointment")
        print("  2. Cancel Appointment")
        print("  3. Reschedule Appointment")
        print("  4. View All Appointments (sorted by date)")
        print("  5. View Patient Appointments")
        print("  6. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                pid = _input("Patient ID: ")
                did = _input("Doctor ID: ")
                date = _input("Date (YYYY-MM-DD): ")
                time = _input("Time (HH:MM): ")
                appt = hospital.book_appointment(pid, did, date, time)
                appt.display()
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            try:
                aid = _input("Appointment ID: ")
                hospital.cancel_appointment(aid)
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "3":
            try:
                aid = _input("Appointment ID: ")
                new_date = _input("New Date (YYYY-MM-DD): ")
                new_time = _input("New Time (HH:MM): ")
                hospital.reschedule_appointment(aid, new_date, new_time)
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "4":
            sorted_appts = hospital.get_appointments_sorted_by_date()
            if not sorted_appts:
                print("  No appointments scheduled.")
            else:
                print(f"\n  All Appointments ({len(sorted_appts)} total):\n")
                for a in sorted_appts:
                    status_label = {
                        "Scheduled": "[SCH]",
                        "Cancelled": "[CAN]",
                        "Completed": "[COM]",
                        "Rescheduled": "[RES]",
                    }.get(a.status, "[???]")
                    print(f"  {status_label} {a}")

        elif choice == "5":
            pid = _input("Patient ID: ")
            appts = [a for a in hospital.appointments if a.patient_id == pid]
            if not appts:
                print(f"  No appointments found for {pid}.")
            else:
                print(f"\n  Appointments for {pid}:\n")
                for a in sorted(appts, key=lambda x: x.appointment_date):
                    print(f"  • {a}")

        elif choice == "6":
            break
        else:
            print("  Invalid choice.")
        _pause()


def menu_pharmacy(hospital: Hospital) -> None:
    while True:
        _print_header("Pharmacy Management")
        print("  1. Add Medicine")
        print("  2. Update Stock (Add)")
        print("  3. Update Stock (Reduce)")
        print("  4. Check Medicine Availability & Expiry")
        print("  5. List All Medicines (sorted by price)")
        print("  6. Check All Expiry Dates")
        print("  7. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                mname = _input("Medicine Name: ")
                stock = int(_input("Initial Stock: "))
                price = float(_input("Price per unit ($): "))
                expiry = _input("Expiry Date (YYYY-MM-DD): ")
                med = hospital.add_medicine(mname, stock, price, expiry)
                med.display()
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            try:
                mid = _input("Medicine ID: ")
                qty = int(_input("Quantity to add: "))
                hospital.update_medicine_stock(mid, qty, "add")
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "3":
            try:
                mid = _input("Medicine ID: ")
                qty = int(_input("Quantity to reduce: "))
                hospital.update_medicine_stock(mid, qty, "reduce")
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "4":
            mid = _input("Medicine ID: ")
            meds = hospital.medicines
            if mid not in meds:
                print("  ERROR: Medicine not found.")
            else:
                meds[mid].display()

        elif choice == "5":
            # Lambda: sort by price
            sorted_meds = hospital.get_medicines_sorted_by_price()
            if not sorted_meds:
                print("  No medicines in inventory.")
            else:
                print(f"\n  Medicines sorted by price (ascending):\n")
                for i, m in enumerate(sorted_meds, 1):
                    print(f"  {i:>3}. {m}")

        elif choice == "6":
            hospital.check_all_expiry()

        elif choice == "7":
            break
        else:
            print("  Invalid choice.")
        _pause()


def menu_medical_records(hospital: Hospital) -> None:
    while True:
        _print_header("Medical Records Management")
        print("  1. Add Medical Record")
        print("  2. View Records for Patient")
        print("  3. List All Records")
        print("  4. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                pid = _input("Patient ID: ")
                diagnosis = _input("Diagnosis: ")
                prescription = _input("Prescription: ")
                notes = _input("Notes (optional, press Enter to skip): ")
                record = hospital.add_medical_record(pid, diagnosis, prescription, notes)
                record.view_record()
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            pid = _input("Patient ID: ")
            records = hospital.get_records_for_patient(pid)
            if not records:
                print(f"  No records found for patient {pid}.")
            else:
                for r in records:
                    r.view_record()

        elif choice == "3":
            records = hospital.medical_records
            if not records:
                print("  No medical records on file.")
            else:
                print(f"\n  Total records: {len(records)}\n")
                for r in records:
                    print(f"  • {r}")

        elif choice == "4":
            break
        else:
            print("  Invalid choice.")
        _pause()


def menu_lab_reports(hospital: Hospital) -> None:
    while True:
        _print_header("Laboratory Reports")
        print("  1. Generate New Lab Report")
        print("  2. View Patient Lab Reports")
        print("  3. View All Reports (Generator)")
        print("  4. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                pid = _input("Patient ID: ")
                test = _input("Test Name: ")
                result = _input("Result: ")
                report = hospital.generate_lab_report(pid, test, result)
                report.display_report()
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            pid = _input("Patient ID: ")
            reports = hospital.get_reports_for_patient(pid)
            if not reports:
                print(f"  No lab reports for patient {pid}.")
            else:
                for r in reports:
                    r.display_report()

        elif choice == "3":
            # Generator usage
            print(f"\n  Streaming all lab reports one by one...\n")
            count = 0
            for report in hospital.yield_lab_reports():
                report.display_report()
                count += 1
            if count == 0:
                print("  No lab reports available.")
            else:
                print(f"  Total reports streamed: {count}")

        elif choice == "4":
            break
        else:
            print("  Invalid choice.")
        _pause()


def menu_billing(hospital: Hospital) -> None:
    while True:
        _print_header("Billing Management")
        print("  1. Generate Bill for Patient")
        print("  2. View Bills for Patient")
        print("  3. View All Bills (Generator)")
        print("  4. Mark Bill as Paid")
        print("  5. Back to Main Menu")
        choice = _input("Enter choice: ")

        if choice == "1":
            try:
                pid = _input("Patient ID: ")
                c_fee = float(_input("Consultation Charge ($): "))
                m_fee = float(_input("Medicine Charge ($): "))
                l_fee = float(_input("Lab Charge ($): "))
                bill = hospital.generate_bill(pid, c_fee, m_fee, l_fee)
                bill.generate_receipt()
            except (ValueError, TypeError) as e:
                print(f"\n  ERROR: {e}")

        elif choice == "2":
            pid = _input("Patient ID: ")
            bills = hospital.get_bills_for_patient(pid)
            if not bills:
                print(f"  No bills found for patient {pid}.")
            else:
                for b in bills:
                    b.generate_receipt()

        elif choice == "3":
            # Generator usage
            print(f"\n  Streaming all bills one by one...\n")
            count = 0
            for bill in hospital.yield_bills():
                print(f"  {bill}")
                count += 1
            if count == 0:
                print("  No bills on file.")
            else:
                print(f"\n  Total bills: {count}")

        elif choice == "4":
            try:
                bid = _input("Bill ID: ")
                bills = hospital.bills
                found = next((b for b in bills if b.bill_id == bid), None)
                if not found:
                    print("  ERROR: Bill not found.")
                else:
                    found.mark_paid()
            except ValueError as e:
                print(f"\n  ERROR: {e}")

        elif choice == "5":
            break
        else:
            print("  Invalid choice.")
        _pause()


# ─── Main Menu ────────────────────────────────────────────────────────────────

def print_main_menu() -> None:
    print(f"\n{'='*55}")
    print(f"     SMART HOSPITAL MANAGEMENT SYSTEM")
    print(f"{'='*55}")
    print(f"  Today: {datetime.datetime.now().strftime('%A, %d %B %Y  %H:%M')}")
    print(f"{'─'*55}")
    print("   1.  Patient Management")
    print("   2.  Doctor Management")
    print("   3.  Nurse Management")
    print("   4.  Appointment Management")
    print("   5.  Pharmacy Management")
    print("   6.  Medical Records")
    print("   7.  Laboratory Reports")
    print("   8.  Billing Management")
    print("   9.  Generate Reports (CSV)")
    print("  10.  Hospital Statistics")
    print("  11.  Hospital Rules")
    print("  12.  Save Data")
    print("  13.  Load Data")
    print("   0.  Exit")
    print(f"{'='*55}")


def main() -> None:
    hospital = Hospital("City Hospital")

    # Try to auto-load saved data on start
    try:
        hospital.load_data()
    except Exception:
        print("  Starting with fresh data.")

    while True:
        print_main_menu()
        choice = _input("Enter choice: ")

        try:
            if choice == "1":
                menu_patient_management(hospital)
            elif choice == "2":
                menu_doctor_management(hospital)
            elif choice == "3":
                menu_nurse_management(hospital)
            elif choice == "4":
                menu_appointment_management(hospital)
            elif choice == "5":
                menu_pharmacy(hospital)
            elif choice == "6":
                menu_medical_records(hospital)
            elif choice == "7":
                menu_lab_reports(hospital)
            elif choice == "8":
                menu_billing(hospital)
            elif choice == "9":
                hospital.generate_reports()
                _pause()
            elif choice == "10":
                Hospital.generate_statistics(hospital)
                _pause()
            elif choice == "11":
                print(Hospital.hospital_rules())
                _pause()
            elif choice == "12":
                hospital.save_data()
                _pause()
            elif choice == "13":
                hospital.load_data()
                _pause()
            elif choice == "0":
                confirm = _input("Save data before exiting? (y/n): ")
                if confirm.lower() == "y":
                    hospital.save_data()
                print("\n  Thank you for using City Hospital Management System. Goodbye!\n")
                sys.exit(0)
            else:
                print("  Invalid choice. Please enter a number from the menu.")

        except KeyboardInterrupt:
            print("\n\n  Operation cancelled by user.")
        except Exception as e:
            print(f"\n  UNEXPECTED ERROR: {e}")


if __name__ == "__main__":
    main()
