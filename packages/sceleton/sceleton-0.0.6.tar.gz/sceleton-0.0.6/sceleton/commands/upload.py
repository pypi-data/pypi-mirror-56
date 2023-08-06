from ..structure.project import project


def upload(project_path, **kwargs):
    """
    Uploads the package in pypi, using `twine upload dist/*`.
    """
    project.upload(project_path)
