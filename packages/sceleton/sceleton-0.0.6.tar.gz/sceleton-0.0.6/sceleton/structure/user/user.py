import os
import sys

from sceleton.structure.project import project, classifier, setup_py

from . import valid


def init(project_name):
    """
    CLI interaction with the user.
    """
    version = input("Choose version (default 0.0.1): ").strip() or "0.0.1"

    description = input("Short description: (required) ").strip()
    author_name = input("Author's name: (required) ").strip()
    author_email = input("Email: (required) ").strip()
    project_url = input("Project url: (required) ")

    keywords = input("Keywords: ").strip() or project_name

    additional_packages = input(
        "Additional packages: \nRemarks: \n"
        + "1. You can add packages later using  `sceleton install [packagelist]` or `sceleton add [packages])\n"
        + "2. Make sure to run `sceleton install` after finishing with initialization of the project.\n"
        + "Packages: "
    ).strip()

    classifiers = (
        input(
            "Add classifiers now, or add some later using\n\
            `sceleton classifiers --edit`? [Y/n]: "
        ).strip()
        or "Y"
    )
    sys.stdout.write("\n\n")

    (
        development_status,
        environment,
        framework,
        auidence,
        license,
        language,
        operating_sys,
        programming_language,
        topic,
    ) = [None] * 9

    if classifiers.lower() in ["y", "yes"]:
        (
            development_status,
            environment,
            framework,
            auidence,
            license,
            language,
            operating_sys,
            programming_language,
            topic,
        ) = select_classifiers()

    return (
        version,
        description,
        author_name,
        author_email,
        project_url,
        keywords,
        additional_packages,
        development_status,
        environment,
        framework,
        auidence,
        license,
        language,
        operating_sys,
        programming_language,
        topic,
    )


def select_classifiers():
    development_status_options = [
        "{} - {}".format(i, dstatus)
        for i, dstatus in enumerate(classifier.DEVELOPMENT_STATUS, 1)
    ]
    development_status_options = "\n".join(development_status_options).strip()
    development_status = input(
        "\n\n\nChoose `Development Status`:\n"
        "\n{}\n".format(development_status_options)
        + "\n\nChoice (Development Status) /enter only the number/: "
    )

    while not valid.range(development_status, classifier.DEVELOPMENT_STATUS):
        development_status = input(
            "Choose a valid number for `Development Status`, between 1 - {}: ".format(
                len(classifier.DEVELOPMENT_STATUS)
            )
        ).strip()

    environment_options = [
        "{} - {}".format(i, environment)
        for i, environment in enumerate(classifier.ENVIRONMENTS, 1)
    ]
    environment_options = "\n".join(environment_options).strip()
    environment = input(
        "\n\nChoose `Environment`:\n"
        + "\n{}\n".format(environment_options)
        + "\n\nChoice (Environment) /enter only the number/: (Can be more than one separated with intervals) "
    )

    while not valid.range(environment.strip(), classifier.ENVIRONMENTS):
        environment = input(
            "Choose a valid number(s) for `Environment`, between 1 - {}: ".format(
                len(classifier.ENVIRONMENTS)
            )
        ).strip()

    framework_options = [
        "{} - {}".format(i, framework)
        for i, framework in enumerate(classifier.FRAMEWORKS, 1)
    ]
    framework_options = "\n".join(framework_options).strip()
    framework = input(
        "\n\nChoose `Framework`: \n"
        + "\n{}\n".format(framework_options)
        + "\n\nChoice (Framework) /enter only the number/: (Can be more than one separated with intervals)  "
    )

    while not valid.range(framework.strip(), classifier.FRAMEWORKS):
        framework = input(
            "Choose a valid number for `Framework`, between 1 - {}: ".format(
                len(classifier.FRAMEWORKS)
            )
        ).strip()

    auidence_options = [
        "{} - {}".format(i, auidence)
        for i, auidence in enumerate(classifier.AUDIENCE, 1)
    ]
    auidence_options = "\n".join(auidence_options).strip()
    auidence = input(
        "\n\nChoose `Intended Audience` (enter only the number) : \n"
        + "\n{}\n".format(auidence_options)
        + "\n\nChoice (Intended Audience): (Can be more than one separated with intervals) "
    )

    while not valid.range(auidence, classifier.AUDIENCE):
        auidence = input(
            "Choose a valid number(s) for `Intended Audience`, between 1 - {}: ".format(
                len(classifier.AUDIENCE)
            )
        ).strip()

    license_options = [
        "{} - {}".format(i, license) for i, license in enumerate(classifier.LICENSES, 1)
    ]
    license_options = "\n".join(license_options).strip()
    license = input(
        "\n\nChoose `License`: \n"
        + "\n{}\n".format(license_options)
        + "\n\nChoice (License) /enter only the number/: "
    )

    while not valid.range(license, classifier.LICENSES):
        license = input(
            "Choose a valid number for `License`, between 1 - {}: ".format(
                len(classifier.LICENSES)
            )
        ).strip()

    language_options = [
        "{} - {}".format(i, language)
        for i, language in enumerate(classifier.LANGUAGES, 1)
    ]
    language_options = "\n".join(language_options).strip()
    language = input(
        "\n\nChoose `Natural Language`: \n"
        + "\n{}\n".format(language_options)
        + "\n\nChoice (Natural Language) /enter only the number/: (Can be more than one separated with intervals) "
    )

    while not valid.range(language, classifier.LANGUAGES):
        language = input(
            "\nChoose a valid number for `Natural Language`, between 1 - {}: ".format(
                len(classifier.LANGUAGES)
            )
        ).strip()

    os_options = ["{} - {}".format(i, os) for i, os in enumerate(classifier.OS, 1)]
    os_options = "\n".join(os_options).strip()
    operating_sys = input(
        "\n\nChoose `Operating System`: \n"
        + "\n{}\n".format(os_options)
        + "\n\nChoice (Operating System) /enter only the number/: (Can be more than one separated with intervals) "
    )

    while not valid.range(operating_sys, classifier.OS):
        operating_sys = input(
            "Choose a valid number for `Operating system`, between 1 - {}: ".format(
                len(classifier.OS)
            )
        )

    pl_options = [
        "{} - {}".format(i, programming_language)
        for i, programming_language in enumerate(classifier.PROGRAMMING_LANGUAGES, 1)
    ]
    pl_options = "\n".join(pl_options).strip()
    programming_language = input(
        "\n\nChoose `Programming language`: \n"
        + "\n{}\n".format(pl_options)
        + "\n\nChoice (Programming Language) /enter only the number/: (Can be more than one separated with intervals) "
    )

    while not valid.range(programming_language, classifier.PROGRAMMING_LANGUAGES):
        programming_language = input(
            "Choose a valid number for `Programming Language`, between 1 - {}: ".format(
                len(classifier.PROGRAMMING_LANGUAGES)
            )
        ).strip()

    topic_options = [
        "{} - {}".format(i, topic) for i, topic in enumerate(classifier.TOPICS, 1)
    ]
    topic_options = "\n".join(topic_options).strip()
    topic = input(
        "\n\nChoose `Topic`: \n"
        + "\n{}\n".format(topic_options)
        + "\n\nChoice (Topic) /enter only the number/: (Can be more than one separated with intervals) "
    )

    while not valid.range(topic, classifier.TOPICS):
        topic = input(
            "Choose a valid number for `Topic`, between 1 - {}: ".format(
                len(classifier.TOPICS)
            )
        ).strip()

    return (
        development_status,
        environment,
        framework,
        auidence,
        license,
        language,
        operating_sys,
        programming_language,
        topic,
    )


def author():
    author = input("Author: ")
    return author


def email():
    email = input("Email: ")
    return email


def license():
    licenses = classifier.LICENSES

    license_options = [
        "{} - {}".format(i, license) for i, license in enumerate(classifier.LICENSES, 1)
    ]
    license_options = "\n".join(license_options).strip()
    license = input(
        "\n\nChoose `License`: \
                          \n{}\n\nChoice (License) /enter only the number/: ".format(
            license_options
        )
    )

    while not valid.range(license, classifier.LICENSES):
        license = input(
            "Choose a valid number for `License`, between 1 - {}: ".format(
                len(classifier.LICENSES)
            )
        ).strip()

    if not license:
        return ""

    return license


def keywords():
    new_keywords = input("Choose one or more keywords: ")
    return new_keywords
