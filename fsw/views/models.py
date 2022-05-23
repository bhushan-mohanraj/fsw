"""
Views to create, read, update, and delete model instances.
"""

import typing

import flask.views
import sqlalchemy.orm
import wtforms

from fsw.views.forms import FormView
from fsw.views.redirects import RedirectView
from fsw.views.templates import TemplateView


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


class ReadModelView(ModelInstanceViewMixin, TemplateView):
    """
    A view that reads model instances.
    """

    def get_template_context(self) -> dict:
        """
        Add the model instances to the template context.
        """

        template_context = TemplateView.get_template_context(self)
        template_context["model_instances"] = self.request_model_instances

        return template_context

    def dispatch_request(self, **kwargs):
        """
        Get the model instances and dispatch the request.
        """

        self.request_model_instances = self.get_model_instances()

        return TemplateView.dispatch_request(self)


class ReadOneModelView(OneModelInstanceViewMixin, TemplateView):
    """
    A view that reads one model instance.
    """

    def get_template_context(self) -> dict:
        """
        Add the model instance to the template context.
        """

        template_context = TemplateView.get_template_context(self)
        template_context["model_instance"] = self.request_model_instance

        return template_context

    def dispatch_request(self, **kwargs):
        """
        Get the model instance and dispatch the request.
        """

        self.request_model_instance = self.get_model_instance()

        return TemplateView.dispatch_request(self)


class CreateModelView(OneModelInstanceViewMixin, FormView):
    """
    A view that creates and saves a model instance.
    """

    def get_model_instance(self):
        """
        Create a new instance of the model class.
        """

        return self.model()

    def _dispatch_valid_form_request(self):
        """
        Internally process a request with valid form data.
        """

        self.request_model_instance = self.get_model_instance()
        self.request_form_instance.populate_obj(self.request_model_instance)

        self.dispatch_valid_form_request()

        self.database_session.add(self.request_model_instance)
        self.database_session.commit()

        return RedirectView.dispatch_request(self)
