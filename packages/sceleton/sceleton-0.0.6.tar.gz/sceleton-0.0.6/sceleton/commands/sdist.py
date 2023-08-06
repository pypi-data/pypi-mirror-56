from ..structure.project import project


def sdist(project_path, **kwargs):
    """
    Builds the project using `python3 setup.py sdist` command.
    """
    project.sdist(project_path)
