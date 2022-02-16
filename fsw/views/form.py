"""
A view class to render and process forms.
"""

import flask.views

from fsw.views.redirect import RedirectView
from fsw.views.template import TemplateView


class FormView(TemplateView, RedirectView, flask.views.View):
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

        Additional form validation should occur through the form.
        """

    def _dispatch_valid_form_request(self):
        """
        Internally process a request with valid form data.
        """

    def dispatch_invalid_form_request(self):
        """
        Process a request with invalid form data.
        """

    def _dispatch_invalid_form_request(self):
        """
        Internally process a request with invalid form data.
        """

    def dispatch_request(self, **kwargs):
        """
        Render the form template for a GET request,
        and process the form data for a POST request.
        """
