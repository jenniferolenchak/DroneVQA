# Python Virtual Environment Setup Tool.
# Note: This has only been tested on Windows. Linux and Mac OS results may vary

import subprocess, os, venv

ENVIRONMENT_DIRECTORY = "./venv"
REQUIREMENTS_FILENAME = "requirements.txt"

try:
    print("Creating Environment")
    venv.create(env_dir=ENVIRONMENT_DIRECTORY, with_pip=True)
    print("Environment Created")
except:
    print("Unable to Create Environment. Did you activate your Virtual Environment already?")

# Install the requirements from a requirements.txt file
if os.path.exists(REQUIREMENTS_FILENAME):
    print("Found Requirements file")
    print("Installing Dependencies")
    subprocess.run([r"./venv/Scripts/python.exe", "-m", "pip", "install", "-r", f"{REQUIREMENTS_FILENAME}"])
else:
    print("No Requirements File Found")
