"""Launcher for the Smart Hospital Management System."""
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "hospital_management.main"], check=True)
