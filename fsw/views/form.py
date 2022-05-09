"""
A view class to render and process forms.
"""

import typing

import flask
import flask.views
import wtforms

from fsw.views.redirect import RedirectView, RedirectViewMixin
from fsw.views.template import TemplateView, TemplateViewMixin


class FormViewMixin(TemplateViewMixin, RedirectViewMixin):
    """
    A mixin for views that render and process a form.
    """

    # The form class.
    form: typing.Type[wtforms.Form]

    # The form instance for the current request.
    # When rendering templates with Jinja, the form instance
    # is accessible as the context variable `form_instance`.
    request_form_instance: wtforms.Form

    def get_template_context(self) -> dict:
        """
        Add the form instance to the template context.
        """

        template_context = TemplateViewMixin.get_template_context(self)
        template_context["form_instance"] = self.request_form_instance

        return template_context

    def get_form() -> typing.Type[wtforms.Form]:
        """
        Get the form class.
        """

        return self.form

    def get_form_instance(self) -> wtforms.Form:
        """
        Get the form instance for GET and POST requests.
        """

        form = self.get_form()

        if flask.request.method == "POST":
            return form(flask.request.form)

        return form()

    def validate_form_instance(self) -> bool:
        """
        Validate the form instance with its submitted data.
        """

        return self.request_form_instance.validate()

    def dispatch_valid_form_request(self) -> None:
        """
        Process a request with valid form data.
        """

    def _dispatch_valid_form_request(self):
        """
        Internally process a request with valid form data.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        self.dispatch_valid_form_request()

        return RedirectView.dispatch_request(self)

    def dispatch_invalid_form_request(self) -> None:
        """
        Process a request with invalid form data.
        """

    def _dispatch_invalid_form_request(self):
        """
        Internally process a request with invalid form data.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        self.dispatch_invalid_form_request()

        return TemplateView.dispatch_request(self)


class FormView(FormViewMixin, flask.views.View):
    """
    A view that renders and processes a form.
    """

    def dispatch_request(self, **kwargs):
        """
        Render the form template for a GET request,
        and process the form data for a POST request.
        """

        self.request_form_instance = self.get_form_instance()

        # Process a request with submitted form data.
        if flask.request.method == "POST":
            # Dispatch a request with valid form data.
            if self.validate_form_instance():
                return self._dispatch_valid_form_request()

            # Dispatch a request with invalid form data.
            return self._dispatch_invalid_form_request()

        # Render the template with the form for GET requests.
        return TemplateView.dispatch_request(self)
