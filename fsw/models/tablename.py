"""
Mixins that automatically set the table name for each model.
"""

import sqlalchemy.orm


class ClassNameModelMixin:
    """
    A mixin that sets the table name of this model
    to its Python class name.
    """

    @sqlalchemy.orm.declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        return cls.__name__
