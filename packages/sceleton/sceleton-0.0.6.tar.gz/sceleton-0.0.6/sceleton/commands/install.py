import json
import re

from ..structure.project import package, setup_py, readme, license


def install(project_path, **kwargs):
    """
    Installs all packages given as option, or gets all of the packages in setup.py and installs them.
    """
    sub_options = kwargs.get("sub_options", {})
    packages = kwargs.get("packages", get_setup_py_packages(project_path))

    if not "--no-add" in sub_options:
        setup_py.packages(
            option="add", package_names=packages, project_path=project_path
        )

    package.install(packages)


def get_setup_py_packages(project_path):
    packages, _ = setup_py.get(type_field="install_requires", project_path=project_path)

    regex = re.compile("\[.*\]")
    packages = (
        regex.findall(packages)[0].replace("'", "*").replace('"', "'").replace("*", '"')
    )
    packages = json.loads(packages)
    return packages
