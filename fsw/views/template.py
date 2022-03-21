"""
A view to render a template with context.
"""

import flask
import flask.views


class TemplateMixin:
    """
    A mixin for views that render a template with context.
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
        run before or after behavior implemented by view subclasses.
        """

        return self.get_template_context()


class TemplateView(flask.views.View, TemplateMixin):
    """
    A view that renders a template with context.
    """

    def dispatch_request(self, **kwargs):
        """
        Render the template with the template context.
        """

        return flask.render_template(
            self.template_name,
            **self._get_template_context(),
        )
