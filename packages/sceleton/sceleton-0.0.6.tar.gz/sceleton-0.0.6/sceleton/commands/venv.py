from ..structure.project import venv as v


def venv(project_path, **kwargs):
    """
    Creates a new virtualenv, using `python3 -m venv venv` as command.
    """
    v.init(project_path)
