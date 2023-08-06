import os

from ..structure.project import project


def module(project_path, **kwargs):
    """
    Creates a module at the given path.
    """
    sub_options = kwargs.get("sub_options", {})
    del kwargs["sub_options"]

    module = os.path.join(project_path, project_path.split(os.sep)[-1])

    parent_module = kwargs.get("parent_module", module)
    if "parent_module" in kwargs:
        for subdir, _, _ in os.walk(module):
            if parent_module in subdir:
                parent_module = subdir
                break

    if "--add" in sub_options:
        project.module(
            project_path,
            kwargs["module_name"],
            parent_module=parent_module,
            files=kwargs["selected_files"],
        )
    else:
        project.module(project_path, kwargs["module_name"], parent_module=parent_module)
