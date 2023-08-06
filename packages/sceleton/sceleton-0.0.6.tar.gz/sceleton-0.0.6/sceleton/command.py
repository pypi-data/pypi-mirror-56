import os
import sys

from .structure.project import classifier

from .commands import *

classifier.init()

COMMANDS = {
    "new": new,
    "init": init,
    "module": module,
    "install": install,
    "classifiers": classifiers,
    "add": add,
    "remove": remove,
    "user": user,
    "license": license,
    "keywords": keywords,
    "venv": venv,
    "upload": upload,
    "local": local,
    "build": build,
    "sdist": sdist,
}


def exec(*args, **kwargs):

    args = list(args)
    command = args[1]
    args.remove(command)

    kwargs.update({"sub_options": args, "version": "0.0.1"})
    current_path = os.getcwd()
    project_path = kwargs.get("--path", current_path) or current_path

    if kwargs["--debug"]:
        COMMANDS.get(command, lambda func: None)(project_path, **kwargs)
    else:
        try:
            COMMANDS.get(command, lambda func: None)(project_path, **kwargs)
            sys.stdout.write("\nDone. Enjoy :)\n")
        except Exception as e:
            sys.stdout.write("\nSomething went wrong :(: {}\n".format(str(e)))
