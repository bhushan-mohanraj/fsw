"""
A view class to render and process forms.
"""

import flask
import flask.views

from fsw.views.redirect import RedirectView, RedirectViewMixin
from fsw.views.template import TemplateView, TemplateViewMixin


class FormViewMixin(RedirectViewMixin, TemplateViewMixin):
    """
    A mixin for views that render and process a form.
    """

    # The form class.
    form: type

    # The form instance for the current request.
    request_form_instance = None

    def _get_template_context(self):
        """
        Add the form instance to the template context.
        """

        template_context = TemplateViewMixin._get_template_context(self) or {}

        template_context["form_instance"] = self.request_form_instance

        return template_context

    def validate_form_instance(self) -> bool:
        """
        Perform additional form validation after WTForms.
        """

        return True

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
        run before or after behavior implemented by view subclasses.
        """

        # Run the custom behavior and return if given.
        if response := self.dispatch_valid_form_request():
            return response

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
        run before or after behavior implemented by view subclasses.
        """

        # Run the custom behavior and return if given.
        if response := self.dispatch_invalid_form_request():
            return response

        return TemplateView.dispatch_request(self)


class FormView(flask.views.View, FormViewMixin):
    """
    A view that renders and processes a form.
    """

    def dispatch_request(self, **kwargs):
        """
        Render the form template for a GET request,
        and process the form data for a POST request.
        """

        self.request_form_instance = self.form(flask.request.form)

        # Process a request with submitted form data.
        if flask.request.method == "POST":
            # Dispatch a request with valid form data.
            if self.request_form_instance.validate() and self.validate_form_instance():
                return self._dispatch_valid_form_request()

            # Dispatch a request with invalid form data.
            return self._dispatch_invalid_form_request()

        # Render the template with the form for GET requests.
        return TemplateView.dispatch_request(self)
