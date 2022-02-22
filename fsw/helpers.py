"""
Helper functions used throughout the package.
"""

import warnings


def fill(instance, **kwargs) -> None:
    """
    Fill the attributes of an object instance
    with the given keyword arguments.
    Raise a warning if a given keyword
    does not correspond to an attribute.
    """

    for key, value in kwargs.items():
        if hasattr(instance, key):
            setattr(instance, key, value)
        else:
            warnings.warn(
                f"An instance of '{type(instance).__name__}'"
                "has no attribute '{key}'."
            )
