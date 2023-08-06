"""Magic functions available in task specifications."""


import pickle

from smart_open import open


def get(name):
    """Get a magic function by name or None if not exists."""
    fun = globals().get(name)
    if (fun is not None and fun.__module__ == __name__
            and fun.__name__ != "get"):
        return fun
    return None


def unpickle(filename):
    """Unpickles an object from a given file."""
    with open(filename, "rb") as f:
        return pickle.load(f)
