"""
Mixins for creating, reading, updating, and deleting model instances.

These mixins require that the `session` attribute exists on the model class.
This attribute should be set to the SQLAlchemy database session or scoped session.
"""

import warnings

from sqlalchemy import select

from fsw.helpers import fill


class _BaseCRUDModelMixin:
    """
    The base class for CRUD mixins.
    """

    session = None  # The SQLAlchemy database session or scoped session.


class CreateModelMixin(_BaseCRUDModelMixin):
    """
    Add a `create` class method to create new model instances.
    """

    @classmethod
    def create(cls, **kwargs):
        """
        Create and save a new model instances using the keyword arguments.
        """

        instance = cls()

        fill(instance, **kwargs)

        cls.session.add(instance)
        cls.session.commit()

        return instance


class ReadModelMixin(_BaseCRUDModelMixin):
    """
    Add `read` and `read_one` class methods to read model instances.
    """

    @classmethod
    def _read_statement(cls, **kwargs):
        """
        Construct an SQLAlchemy statement to read rows with certain column values.
        """

        statement = select(cls)

        for key, value in kwargs.items():
            if not hasattr(cls, key):
                warnings.warn(
                    f"An instance of '{cls.__name__}' has no attribute '{key}'."
                )

            statement = statement.where(getattr(cls, key) == value)

        return statement

    @classmethod
    def read(cls, **kwargs) -> list:
        """
        Read all model instances satisfying the keyword arguments.
        """

        statement = cls._read_statement(**kwargs)

        return cls.session.execute(statement).scalars().all()

    @classmethod
    def read_one(cls, **kwargs):
        """
        Read the first model instance satisfying the keyword arguments.
        """

        statement = cls._read_statement(**kwargs)

        return cls.session.execute(statement).scalars().first()


class UpdateModelMixin(_BaseCRUDModelMixin):
    """
    Add an `update` method to update the model instance.
    """

    def update(self, **kwargs):
        """
        Update and save the current model instance using the keyword arguments.
        """

        fill(self, **kwargs)

        self.session.commit()

        return self


class DeleteModelMixin(_BaseCRUDModelMixin):
    """
    Add a `delete` method to delete the model instance.
    """

    def delete(self):
        """
        Delete the current model instance.
        """

        self.session.delete(self)
        self.session.commit()
