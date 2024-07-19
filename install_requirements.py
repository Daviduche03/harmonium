import subprocess
import sys
import os

def install_requirements(requirements_file='requirements.txt'):
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found.")
        return False

    try:
        # Check if pip is installed
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
    except subprocess.CalledProcessError:
        print("Error: pip is not installed or not in the system PATH.")
        return False

    print(f"Installing requirements from {requirements_file}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("All requirements installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing requirements: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        requirements_file = sys.argv[1]
    else:
        requirements_file = 'requirements.txt'
    
    success = install_requirements(requirements_file)
    sys.exit(0 if success else 1)