"""
Views to create, read, update, and delete model instances.
"""

class ModelViewMixin:
    """
    A mixin for views that process an SQLAlchemy model class.
    """

    # The SQLAlchemy database session.
    database_session: None

    # The model class.
    model: type


class ModelInstanceViewMixin(_ModelViewMixin):
    """
    A mixin for views that process one model instance.
    """

    # The current model instance (during request dispatching).
    model_instance = None

    def get_model_instance(self):
        """
        Get the model instance.
        """

        return None


class ModelInstancesViewMixin(_ModelViewMixin):
    """
    A mixin for views that process multiple model instances.
    """

    # The current model instances (during request dispatching).
    model_instances = []

    def get_model_instances(self) -> list:
        """
        Get the model instances.
        """

        return []