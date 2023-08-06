from ..structure.project import setup_py


def remove(project_path, **kwargs):
    """
    Removes all given packages from `setup.py`'s list.
    """
    packages = kwargs.get("packages", [])
    setup_py.packages(
        option="remove", package_names=packages, project_path=project_path,
    )
