import sys

from ..structure.project import setup_py
from ..structure.user import user


def keywords(project_path, **kwargs):
    """
    Returns all keywords, or edits them in `setup.py`.
    """
    sub_options = kwargs.get("sub_options", {})
    del kwargs["sub_options"]

    current_keywords, keywords_index = setup_py.get(
        type_field="keywords", project_path=project_path
    )

    sys.stdout.write("\nCurrent keywords\n")
    sys.stdout.write("-" * 15)
    sys.stdout.write("\n")

    current_keywords = current_keywords.split("=")[-1].strip().replace("'", "")
    sys.stdout.write(current_keywords)
    sys.stdout.write("\n\n")

    if "--edit" in sub_options:
        keywords = user.keywords().strip()

        project_name = project_path.split(os.sep)[-1]
        keywords = keywords or project_name
        setup_py.edit("keywords", keywords, project_path, keywords_index)
