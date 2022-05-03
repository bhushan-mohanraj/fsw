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
    request_form_instance: wtforms.Form

    def _get_template_context(self) -> dict:
        """
        Add the form instance to the template context.
        """

        template_context = TemplateViewMixin._get_template_context(self) or {}

        template_context["form_instance"] = self.request_form_instance

        return template_context

    def get_form_instance(self) -> wtforms.Form:
        """
        Get the new form instance for both GET and POST requests.

        Unless this method returns a custom form instance,
        the view creates an empty form instance for GET requests
        and creates an instance from the POST data for POST requests.
        """

    def _get_form_instance(self) -> wtforms.Form:
        """
        Internally get the new form instance for both GET and POST requests.
        """

        if form_instance := self.get_form_instance():
            return form_instance

        if flask.request.method == "POST":
            return self.form(flask.request.form)

        return self.form()

    def validate_form_instance(self) -> bool:
        """
        Perform additional form validation after WTForms.
        """

        return True

    def _validate_form_instance(self) -> bool:
        """
        Internally perform additional form validation after WTForms.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        return self.validate_form_instance()

    def dispatch_valid_form_request(self):
        """
        Process a request with valid form data.

        Unless this method returns a custom response,
        the view redirects to the given URL.
        """

    def _dispatch_valid_form_request(self):
        """
        Internally process a request with valid form data.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        # Run the custom behavior and return the response if given.
        if response := self.dispatch_valid_form_request():
            return response

        return RedirectView.dispatch_request(self)

    def dispatch_invalid_form_request(self):
        """
        Process a request with invalid form data.

        Unless this method returns a custom response,
        the view renders the given template with the form.
        """

    def _dispatch_invalid_form_request(self):
        """
        Internally process a request with invalid form data.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        # Run the custom behavior and return the response if given.
        if response := self.dispatch_invalid_form_request():
            return response

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

        self.request_form_instance = self._get_form_instance()

        # Process a request with submitted form data.
        if flask.request.method == "POST":
            # Dispatch a request with valid form data.
            if self.request_form_instance.validate() and self._validate_form_instance():
                return self._dispatch_valid_form_request()

            # Dispatch a request with invalid form data.
            return self._dispatch_invalid_form_request()

        # Render the template with the form for GET requests.
        return TemplateView.dispatch_request(self)
