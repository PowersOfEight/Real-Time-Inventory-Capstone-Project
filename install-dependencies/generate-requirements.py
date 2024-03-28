import ast
import os
import sys
import subprocess

SAVE_PATH = 'install-dependencies/requirements.txt'

def generate_requirements() -> int:
    exit_code = 0
    current_directory = os.getcwd()
    print("Current directory: " + current_directory)
    print("Changing directories...")
    os.chdir(r'..')
    print("Current directory: " + os.getcwd() + "\n")
    try:
        subprocess.check_call( ["pipreqs", "--version"])
        subprocess.check_call( ["pipreqs","--force","--savepath",SAVE_PATH, "."])
    except subprocess.CalledProcessError:
        print("pipreqs not installed")
        exit_code = 1
    finally:
        os.chdir(current_directory)
        return exit_code

def pip_install_pipreqs():
    try:
        subprocess.check_call([sys.executable, "-m", "pip","install", "pipreqs"])
    except subprocess.CalledProcessError as er:
        print(f'Problem installing package pipreqs: {er}')

def check_pip_installed() -> bool:
    try:
        subprocess.check_call([sys.executable, "-m" , "pip", "--version"])
    except subprocess.CalledProcessError:
        print("pip not installed.  Please install pip and try again")
        sys.exit(1)
    return True

if __name__ == "__main__":
    if check_pip_installed():
        print("pip installed, proceed")
    generate_requirements()
