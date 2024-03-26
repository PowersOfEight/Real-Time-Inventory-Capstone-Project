import subprocess
import sys
import os

def install_dependencies():
    # Check if pip is installed
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
    except subprocess.CalledProcessError:
        print("pip is not installed. Please install pip (Python package manager) first.")
        sys.exit(1)

    # Install dependencies
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please check for errors.")
        sys.exit(1)

    print("Dependencies installed successfully.")

if __name__ == "__main__":
    # Change directory to the script's directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Call the function to install dependencies
    install_dependencies()
