"""
A mixin that sets the table name to the class name of a model.
"""

import sqlalchemy.orm


class ClassNameModelMixin:
    """
    A mixin that sets the database table name to the class name of a model.
    """

    @sqlalchemy.orm.declared_attr
    def __tablename__(cls):
        return cls.__name__
