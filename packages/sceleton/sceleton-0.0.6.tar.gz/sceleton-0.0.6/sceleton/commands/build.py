from ..structure.project import project


def build(project_path, **kwargs):
    """
    Builds the project using `python3 setup.py build` command.
    """
    project.build(project_path)
