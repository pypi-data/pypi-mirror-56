import subprocess

from . import sceleton


def ignore(project_name):
    gitignore = sceleton("gitignore.txt")
    gitignore.append("{}.egg-info".format(project_name))
    gitignore = "".join(gitignore)
    return gitignore


def init(project_path):
    subprocess.run(["git", "init", project_path])
