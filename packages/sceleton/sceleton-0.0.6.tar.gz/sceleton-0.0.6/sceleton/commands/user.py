import sys

from ..structure.user import user as user_
from ..structure.project import setup_py


def user(project_path, **kwargs):
    """
    Returns information about current owner of the project, or edits it.
    """
    sub_options = kwargs.get("sub_options", {})
    del kwargs["sub_options"]

    author = "author"
    email = "author_email"

    author_name, author_index = setup_py.get(
        type_field=author, project_path=project_path
    )
    author_email, email_index = setup_py.get(
        type_field=email, project_path=project_path
    )

    sys.stdout.write("\nCurrent author\n")
    sys.stdout.write("-" * 15)

    author_name = author_name.strip()[len(author) + 1 :].replace("'", "")

    sys.stdout.write("\nName: ".ljust(11) + author_name.ljust(20))
    sys.stdout.write("\n")
    author_email = author_email.lstrip()[len(email) + 1 :].replace("'", "")
    sys.stdout.write("Email: ".ljust(10) + author_email.ljust(20))
    sys.stdout.write("\n\n")

    if "--edit" in sub_options:
        sys.stdout.write("Enter your new name and new email: \n")
        new_name, new_email = user_.author(), user_.email()
        setup_py.edit(author, new_name, project_path, author_index)
        setup_py.edit(email, new_email, project_path, email_index)
