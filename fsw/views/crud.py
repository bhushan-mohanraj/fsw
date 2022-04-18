"""
Views to create, read, update, and delete model instances.
"""

import sqlalchemy.orm


class _ModelViewMixin:
    """
    A mixin for views that process an SQLAlchemy model class.
    """

    # The SQLAlchemy database session.
    database_session: sqlalchemy.orm.scoped_session

    # The model class.
    model: type


class _ModelInstanceViewMixin(_ModelViewMixin):
    """
    A mixin for views that process model instances.
    """

    # The model instances for the current request.
    request_model_instances = []

    def get_model_instances(self) -> list:
        """
        Get the model instances.
        """

        raise NotImplementedError


class _OneModelInstanceViewMixin(_ModelViewMixin):
    """
    A mixin for views that process one model instance.
    """

    # The model instance for the current request.
    request_model_instance = None

    def get_model_instance(self):
        """
        Get the model instance.
        """

        raise NotImplementedError
