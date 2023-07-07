"""
A view class to render and process forms.
"""

import typing

import flask
import flask.views
import wtforms

from fsw.views.redirects import RedirectView
from fsw.views.templates import TemplateView


class FormView(RedirectView, TemplateView):
    """
    A view that renders and processes a form.
    """

    form_class: typing.Type[wtforms.Form]

    # The form instance for the current request.
    # When rendering templates with Jinja, the form
    # is accessible as the context variable `form`.
    request_form: wtforms.Form

    def get_template_context(self) -> dict:
        """
        Add the form instance to the template context.
        """
        template_context = TemplateView.get_template_context(self)
        template_context["form"] = self.request_form

        return template_context

    def get_form_class(self) -> typing.Type[wtforms.Form]:
        """
        Get the form class.
        """
        return self.form_class

    def get_form(self) -> wtforms.Form:
        """
        Get the form for GET and POST requests.
        """
        form_class = self.get_form_class()

        if flask.request.method == "POST":
            return form_class(flask.request.form)

        return form_class()

    def validate_form(self) -> bool:
        """
        Validate the form with its submitted data.
        """
        return self.request_form.validate()

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

    def dispatch_request(self, **kwargs):
        """
        Render the form template for a GET request,
        and process the form data for a POST request.
        """
        self.request_form = self.get_form()

        # Process a request with submitted form data.
        if flask.request.method == "POST":
            # Dispatch a request with valid form data.
            if self.validate_form():
                return self._dispatch_valid_form_request()

            # Dispatch a request with invalid form data.
            return self._dispatch_invalid_form_request()

        # Render the template with the form for GET requests.
        return TemplateView.dispatch_request(self)
