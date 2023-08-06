from ..structure.project import setup_py


def add(project_path, **kwargs):
    """
    Adds all given packages to the `setup.py` file.
    """
    packages = kwargs.get("packages", [])
    setup_py.packages(
        option="add", package_names=packages, project_path=project_path,
    )
