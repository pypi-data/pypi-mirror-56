import os
import sys

from ..structure.user import user
from ..structure.project import project, classifier, package


def init(project_path, **kwargs):
    """
    Initializes a setup.py file, if a project with given name doesn't exist.
    """
    sub_options = kwargs.get("sub_options", {})
    path = kwargs["--path"] or os.getcwd()
    version = kwargs["version"]
    project_name = kwargs.get("project_name", "")
    if os.path.exists(path) and "setup.py" in os.listdir(path):
        answer = input(
            "There is another `setup.py` file in {}.\nDo you really want to replace it with a new `setup.py` file? [yN]: ".format(
                path
            )
        )

        if answer.lower() != "y" and answer.lower() != "yes":
            return

    if "--quick" in sub_options:
        project.new_setup_py(project_path=path, version=version, license_type="MIT License")
    else:
        (
            version,
            description,
            author_name,
            author_email,
            project_url,
            keywords,
            packages,
            development_status,
            environment,
            framework,
            auidence,
            license_type,
            language,
            operating_sys,
            programming_language,
            topic,
        ) = user.init(project_name)

        classifiers = classifier.format(
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

        if license_type:
            license_type = classifier.LICENSES[int(license_type) - 1].split("::")[-1].strip()

        project.new_setup_py(
            project_path=path,
            version=version,
            author_email=author_email,
            author_name=author_name,
            description=description,
            license_type=license_type,
            classifiers=classifiers,
            keywords=keywords,
            project_url=project_url,
            packages=packages,
        )
