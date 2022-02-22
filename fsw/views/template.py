"""
A view to render a template with context.
"""

import flask
from flask import views


class TemplateView(views.View):
    """
    A view to render a template with context.
    """

    template_name: str = ""

    def get_template_context(self) -> dict:
        """
        Get the context dictionary to render the template.
        """

        return {}

    def _get_template_context(self) -> dict:
        """
        Internally get the context dictionary to render the template.

        Base subclasses can implement this method with custom behavior
        that runs before or after behavior implemented by view subclasses.
        """

        return self.get_template_context()

    def dispatch_request(self, **kwargs) -> flask.Response:
        """
        Render the template with the template context.
        """

        return flask.render_template(
            self.template_name,
            **self._get_template_context(),
        )
