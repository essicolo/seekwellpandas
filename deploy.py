import os
import subprocess
import sys

def deploy_to_pypi():
    try:
        subprocess.check_call([sys.executable, "-m", "build"])
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "twine", 
            "upload", 
            "dist/*"
        ])
        print("Success")
    except subprocess.CalledProcessError as e:
        print(f"Deployement error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    deploy_to_pypi()