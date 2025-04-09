import os
import subprocess
import sys
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

def loading_animation(message: str):
    spinner =  ['|', '/', '-', '\\']
    i = 0
    while not stop_loading:
        sys.stdout.write(f"\r{message} {spinner[i % len(spinner)]}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)

print("\n>--Welcome to the ADCP Setup--<")

# GUI Folder Picker
venv_path = None
try:
    root = tk.Tk()
    root.withdraw()
    venv_path = filedialog.askdirectory(title="Select Folder to Create VENV")

    if not venv_path:
        messagebox.showinfo("Cancelled", "Setup cancelled by this guy.")
        print("\n>--Setup cancelled--<")
        sys.exit(0)
except Exception:
    print("⚠ GUI selection failed. Falling back to terminal input.")
    venv_path = input("Enter the full path for venv manually: ").strip()
    if not venv_path:
        print("\n>--No path provided. Exiting.--<")
        sys.exit(1)

# Define full path to ADCP venv
venv_dir = os.path.join(venv_path, "ADCP")

# Check if venv already exists
if os.path.exists(venv_dir):
    print(f"\n>--Virtual environment 'ADCP' already exists Sir at: {venv_dir}--<")
    print(">--Skipping venv creation--<\n")
else:
    # Create venv with animation
    print(f"\nCreating virtual environment at: {venv_dir} ...")
    stop_loading = False
    thread = threading.Thread(target=loading_animation, args=("Creating virtual environment",))
    thread.start()

    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    finally:
        stop_loading = True
        thread.join()
        print("\r>--Virtual environment created successfully--<\n")

# Step 2: Install requirements
print("\n>--Calling package injector--<")
this_dir = os.path.dirname(os.path.abspath(__file__))
step_1_script = os.path.join(this_dir, "install_req.py")
subprocess.check_call([sys.executable, step_1_script, venv_dir])