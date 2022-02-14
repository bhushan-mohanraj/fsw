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

    def dispatch_request(self, **kwargs) -> flask.Response:
        """
        Render the template with the template context.
        """

        return flask.render_template(
            self.template_name,
            **self.get_template_context(),
        )
