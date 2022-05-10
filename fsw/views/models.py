"""
Views to create, read, update, and delete model instances.
"""

import typing

import sqlalchemy.orm


class ModelViewMixin:
    """
    A mixin for views that process an SQLAlchemy model class.
    """

    # The SQLAlchemy database session.
    database_session: sqlalchemy.orm.scoped_session

    # The model class.
    model: type


class ModelInstanceViewMixin(ModelViewMixin):
    """
    A mixin for views that process model instances.
    """

    # The model instances for the current request.
    # When rendering templates with Jinja, the list of model instances
    # is accessible as the context variable `model_instances`.
    request_model_instances: list

    def get_model_instances(self) -> list:
        """
        Get the model instances.
        """

        raise NotImplementedError


class OneModelInstanceViewMixin(ModelViewMixin):
    """
    A mixin for views that process one model instance.
    """

    # The model instance for the current request.
    # When rendering templates with Jinja, the model instance
    # is accessible as the context variable `model_instance`.
    request_model_instance: typing.Any

    def get_model_instance(self):
        """
        Get the model instance.
        """

        raise NotImplementedError
