import os


def missing(file):
    """
    Mostly used for checking if `setup.py` file is missing.
    """

    def wrapper(func):
        def _args(*args, **kwargs):
            files = os.listdir(args[0])
            if not file in files:
                raise FileNotFoundError("{} is not found.".format(file))
            return func(*args, **kwargs)

        return _args

    return wrapper
