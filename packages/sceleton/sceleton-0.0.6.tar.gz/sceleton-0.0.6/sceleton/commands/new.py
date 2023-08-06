import os
import sys

from ..structure.user import user
from ..structure.project import project, classifier, package


def new(project_path, **kwargs):
    """
    Creates a new project, depending from the given options.

    :param project_path: is the path given by the user. If no path is provided, then user's current path is used.
    :param sub_options: possible suboptions are:
        * `--django` for a new django project, which will install the latest version of django.
        *  `--quick` which will not ask the user for additional information, with which populates the `setup.py` file.
        *  `--virtualenv` which will initialize a new virtual env in the user's project folder.
        If suboptions doesn't include `--quick`, user must answer all questions included in the `structure -> user -> select_classifiers` method.
    :kwargs:
    :kwarg project_name: is the name of the project of the user, if such folder already exists in the
        user's folder of choice, FileExistsError will be thrown.
    """
    sub_options = kwargs.get("sub_options", {})
    version = kwargs.get("version", "0.0.1")
    project_name = kwargs.get("project_name", "")

    if os.path.exists(os.path.join(project_path, project_name)):
        raise FileExistsError("File with name {} already exist.".format(project_name))

    virtual_env = any(
        filter(lambda value: value in sub_options, {"--venv", "--virtualenv"})
    )

    if "--django" in sub_options:

        license_type = user.license()
        if license_type:
            license_type = (
                classifier.LICENSES[int(license_type) - 1].split("::")[-1].strip()
            )

        package.install(["django"])
        project.init(
            version=version,
            create_django_project=True,
            project_path=project_path,
            project_name=project_name,
            license_type=license_type,
            set_virtual_env=virtual_env,
        )

    elif "--quick" in sub_options:
        project.init(
            project_path=project_path,
            project_name=project_name,
            version=version,
            set_virtual_env=virtual_env,
        )
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
            license_type = (
                classifier.LICENSES[int(license_type) - 1].split("::")[-1].strip()
            )

        project.init(
            project_path=project_path,
            project_name=project_name,
            version=version,
            author_email=author_email,
            description=description,
            author_name=author_name,
            license_type=license_type,
            classifiers=classifiers,
            keywords=keywords,
            project_url=project_url,
            packages=packages,
            set_virtual_env=virtual_env,
        )
