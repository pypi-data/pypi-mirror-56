import sys

from ..structure.user import user
from ..structure.project import project, classifier, setup_py, readme, license


def classifiers(project_path, **kwargs):
    """
    Returns all classifiers, or edits them.
    """
    sub_options = kwargs.get("sub_options", {})

    current_classifiers, index = setup_py.get(
        type_field="classifiers", project_path=project_path
    )

    current_classifiers = current_classifiers.split("=")[-1].strip()

    sys.stdout.write(
        "\nCurrent classifiers\n{}\n{}\n".format("-" * 15, current_classifiers)
    )

    if "--edit" in sub_options:
        (
            development_status,
            environment,
            framework,
            auidence,
            license_type,
            language,
            operating_sys,
            programming_language,
            topic,
        ) = user.select_classifiers()
        classifiers_ = classifier.format(
            development_status=development_status,
            environment=environment,
            framework=framework,
            auidence=auidence,
            license=license_type,
            language=language,
            operating_sys=operating_sys,
            programming_language=programming_language,
            topic=topic,
        )

        new_license = (
            classifier.LICENSES[int(license_type) - 1].split(" :: ")[-1].strip()
            if license_type
            else "MIT License"
        )

        setup_py.classifiers(project_path, classifiers_, index)
        current_license, index = setup_py.get(
            type_field="license", project_path=project_path
        )
        current_license = (
            current_license.split("=")[-1].strip().replace("'", "").replace(",", "")
        )

        setup_py.edit("license", new_license, project_path, index)
        project.make_file(
            folder_path=project_path,
            filename="LICENSE",
            content=license.init(new_license),
        )

        readme.edit(project_path, old_value=current_license, new_value=new_license)
