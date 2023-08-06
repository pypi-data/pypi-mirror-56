from ..structure.project import project


def local(project_path, **kwargs):
    """
    Installs the project locally, uses the command `python3 setup.py install`.
    """
    project.local(project_path)
