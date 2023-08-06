import pkg_resources
import os

ENCODING = "utf-8"


def sceleton(file):
    global ENCODING
    content_path = os.path.join("skeleton", file)
    content = pkg_resources.resource_string(__name__, content_path)
    return content.decode(ENCODING).split("\n")


def licenses(file):
    global ENCODING
    content_path = os.path.join("licenses", file)
    content = pkg_resources.resource_string(__name__, content_path)
    return content.decode(ENCODING)


def python_v():
    import sys

    return sys.version_info

from . import venv
from . import setup_py
from . import readme
from . import package
from . import git
from . import classifier
from . import license
