"""
A view to render a template with context.
"""

import flask
from flask import views


class TemplateView(views.View):
    """
    A view to render a template with context.
    """

    template_name: str

    def get_template_context(self, **kwargs) -> dict:
        """
        Get the context dictionary to render the template.

        The view arguments are passed to this method.
        This returns all the given keyword arguments by default.
        """

        return kwargs

    def dispatch_request(self, **kwargs) -> flask.Response:
        """
        Render the template with the template context.
        """

        return flask.render_template(
            self.template_name,
            **self.get_template_context(**kwargs),
        )
