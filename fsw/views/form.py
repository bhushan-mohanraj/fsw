"""
A view class to render and process forms.
"""

import flask
import flask.views

from fsw.views.redirect import RedirectMixin, RedirectView
from fsw.views.template import TemplateMixin, TemplateView


class FormView(flask.views.View, RedirectMixin, TemplateMixin):
    """
    A view class to render and process forms.
    """

    # The form class.
    form: type

    # The current form instance.
    form_instance = None

    def _get_template_context(self):
        """
        Add the form instance to the template context.
        """

        # Get the template context provided by developers.
        template_context = self.get_template_context()

        # Add the current form instance to the context.
        template_context["form_instance"] = self.form_instance

        return template_context

    def dispatch_valid_form_request(self):
        """
        Process a request with valid form data.
        If this method returns no custom response,
        the view redirects to the given URL.

        Additional form validation should occur through the form.
        """

    def _dispatch_valid_form_request(self):
        """
        Internally process a request with valid form data.

        Base subclasses can implement this method with custom behavior
        that runs before or after behavior implemented by view subclasses.
        """

        # Run custom behavior for a valid request.
        response = self.dispatch_valid_form_request()

        # Return the custom response if given.
        if response:
            return response

        # Redirect to the given URL.
        return RedirectView.dispatch_request(self)

    def dispatch_invalid_form_request(self):
        """
        Process a request with invalid form data.
        If this method returns no custom response,
        the view renders the given template with the form.
        """

    def _dispatch_invalid_form_request(self):
        """
        Internally process a request with invalid form data.

        Base subclasses can implement this method with custom behavior
        that runs before or after behavior implemented by view subclasses.
        """

        # Run custom behavior for an invalid request.
        response = self.dispatch_invalid_form_request()

        # Return the custom response if given.
        if response:
            return response

        # Render the given template with the form and validation errors.
        return TemplateView.dispatch_request(self)

    def dispatch_request(self, **kwargs):
        """
        Render the form template for a GET request,
        and process the form data for a POST request.
        """

        self.form_instance = self.form(flask.request.form)

        # Process a request with submitted form data.
        if flask.request.method == "POST":
            # Dispatch a request with valid form data.
            if self.form_instance.validate():
                return self._dispatch_valid_form_request()

            # Dispatch a request with invalid form data.
            return self._dispatch_invalid_form_request()

        # Render the template with the form for GET requests.
        return TemplateView.dispatch_request(self)
