import subprocess
import sys
import os

venv_dir = sys.argv[1] if len(sys.argv) > 1 else None
if not venv_dir:
    print(">--VENV path not provided--<")
    sys.exit(1)

# Determine pip executable from venv
pip_exec = os.path.join(venv_dir, "Scripts", "pip.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "pip")

print("\n>--Injecting required packages--<")

required_packages = [
    "pandas",
    "scikit-learn",
    "numpy",
    "polars",
    "pyarrow",
    "openpyxl",
    "python-dotenv",
    "loguru",
    "psycopg2-binary",
    "tk"
]

# Resolve python executable inside venv
python_exec = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "python")

# Upgrade pip using proper module call
subprocess.check_call([
    python_exec,
    "-m",
    "pip",
    "install",
    "--upgrade",
    "pip",
    "--disable-pip-version-check"
])


subprocess.check_call([
    python_exec,
    "-m",
    "pip",
    "install",
    *required_packages
])


# Ask user to select which main file to run
print("\n>--All packages injected successfully--<")
print("\n>--Choose the method--<")
print("1 for Manual data injection")
print("2 for Scheduled DB injection")

choice = input("Enter 1 or 2: ").strip()
entry_script = "main_data_inject.py" if choice == "1" else "main_schedule_inject.py"

python_exec = os.path.join(venv_dir, "Scripts", "python.exe") if os.name == 'nt' else os.path.join(venv_dir, "bin", "python")

print(f"\n>--Running--< {entry_script}...")
subprocess.check_call([python_exec, entry_script])