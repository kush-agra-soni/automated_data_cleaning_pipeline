import os
import subprocess
import sys

print("\n📦 Welcome to the Automated Data Cleaning Pipeline Setup")

# Ask user where to create the venv
venv_path = input("Enter the full path where you'd like to create the virtual environment: ").strip()

# Define venv directory
venv_dir = os.path.join(venv_path, "automated_data_cleaning_pipeline")

# Step 1: Create venv
print(f"\n🔧 Creating virtual environment at: {venv_dir} ...")
subprocess.check_call([sys.executable, "-m", "venv", venv_dir])

# Activate venv command (OS dependent)
activate_cmd = os.path.join(venv_dir, "Scripts", "activate") if os.name == 'nt' else f"source {venv_dir}/bin/activate"

# Step 2: Install requirements via step_1 script
print("\n📥 Proceeding to install required libraries...")
subprocess.check_call([sys.executable, "step_1_install_req.py", venv_dir])
