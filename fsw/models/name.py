"""
A mixin that sets the table name to the class name of a model.
"""

import sqlalchemy.orm


class ClassNameModelMixin:
    """
    Set the table name to the model class name.
    """

    @sqlalchemy.orm.declared_attr
    def __tablename__(cls):
        return cls.__name__
