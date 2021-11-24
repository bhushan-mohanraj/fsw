"""
Mixins for creating, reading, updating, and deleting model objects.

These mixins require that the `session` attribute exists on the model class.
This attribute should be set to the SQLAlchemy database session or scoped session.
"""

from sqlalchemy import select


class _CRUDBaseMixin:
    """
    The base class for CRUD mixins.
    """

    session = None

    def _fill(self, **kwargs):
        """
        Fill the attributes of the object with the given keyword arguments.

        Raise an error if a given keyword argument is not an actual attribute.
        """

        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError(
                    f"'{type(self).__name__}' object has no attribute '{key}'"
                )

            setattr(self, key, value)


class CreateMixin(_CRUDBaseMixin):
    """
    Add a `create` class method to create new model objects.
    """

    @classmethod
    def create(cls, **kwargs):
        """
        Create and save a new model object using the keyword arguments.
        """

        instance = cls()
        instance._fill(**kwargs)

        cls.session.add(instance)
        cls.session.commit()

        return instance


class ReadMixin(_CRUDBaseMixin):
    """
    Add `read` and `read_one` class methods to read model objects.
    """

    @classmethod
    def _read_statement(cls, **kwargs):
        """
        Construct an SQLAlchemy statement to read rows with certain column values.
        """

        statement = select(cls)

        for key, value in kwargs.items():
            if not hasattr(cls, key):
                raise AttributeError(
                    f"'{cls.__name__}' object has no attribute '{key}'"
                )

            statement = statement.where(getattr(cls, key) == value)

        return statement

    @classmethod
    def read(cls, **kwargs) -> list:
        """
        Read all model objects satisfying the keyword arguments.
        """

        statement = cls._read_statement(**kwargs)

        return cls.session.execute(statement).scalars().all()

    @classmethod
    def read_one(cls, **kwargs):
        """
        Read the first model object satisfying the keyword arguments.
        """

        statement = cls._read_statement(**kwargs)

        return cls.session.execute(statement).scalars().first()


class UpdateMixin(_CRUDBaseMixin):
    """
    Add an `update` method to update the model object.
    """

    def update(self, **kwargs):
        """
        Update and save the current model object using the keyword arguments.
        """

        self._fill(**kwargs)

        self.session.commit()

        return self


class DeleteMixin(_CRUDBaseMixin):
    """
    Add a `delete` method to delete the model object.
    """

    def delete(self):
        """
        Delete the current model object.
        """

        self.session.delete(self)
        self.session.commit()


class CRUDMixin(CreateMixin, ReadMixin, UpdateMixin, DeleteMixin):
    """
    A mixin combining the create, read, update, and delete mixins.
    """
