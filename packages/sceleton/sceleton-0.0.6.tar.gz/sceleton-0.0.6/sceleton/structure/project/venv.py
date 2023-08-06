import subprocess
import os

from . import python_v


def init(project_path):
    venv = os.path.join(project_path, "venv")

    if not os.path.exists(venv):
        os.makedirs(venv)

    version = python_v()

    if version < (3, 0, 0):
        subprocess.run(["python3", "-m", "venv", venv, "--without-pip"])
    else:
        subprocess.run(["python", "-m", "venv", venv, "--without-pip"])
