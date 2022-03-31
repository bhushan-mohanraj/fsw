"""
Helper functions used throughout the package.
"""

import warnings


def fill(instance, **kwargs) -> None:
    """
    Fill the attributes of an object instance with the keyword arguments.
    Raise a warning if a given keyword does not correspond to an attribute.
    """

    for key, value in kwargs.items():
        if not hasattr(instance, key):
            raise AttributeError(
                f"An instance of `{type(instance).__name__}`"
                f"has no attribute `{key}`."
            )

        setattr(instance, key, value)
