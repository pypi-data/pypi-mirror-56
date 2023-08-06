import sys

from ..structure.user import user
from ..structure.project import project, classifier, setup_py, readme
from ..structure.project import license as license_


def license(project_path, **kwargs):
    """
    Returns current license, or edits it in `setup.py`, `LICENSE` and `README.rst`.
    """
    sub_options = kwargs.get("sub_options", {})
    del kwargs["sub_options"]

    current_license, index = setup_py.get(
        type_field="license", project_path=project_path
    )

    sys.stdout.write("\nCurrent license\n")
    sys.stdout.write("-" * 15)
    sys.stdout.write("\n")

    current_license = (
        current_license.split("=")[-1].strip().replace("'", "").replace(",", "")
    )

    sys.stdout.write(current_license)
    sys.stdout.write("\n")

    if "--edit" in sub_options:
        new_license = user.license().strip()
        new_license = (
            classifier.LICENSES[int(new_license) - 1] if new_license else "MIT License"
        )
        new_license_name = new_license.split(" :: ")[-1].strip()
        setup_py.edit("license", new_license_name, project_path, index)
        setup_py.edit_classifier_license(project_path, current_license, new_license)
        project.make_file(
            folder_path=project_path,
            filename="LICENSE",
            content=license_.init(new_license_name),
        )
        readme.edit(project_path, old_value=current_license, new_value=new_license_name)
