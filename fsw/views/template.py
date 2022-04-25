"""
A view to render a template with context.
"""

import flask
import flask.views


class TemplateViewMixin:
    """
    A mixin for views that render a template with context.
    """

    # The Flask template name to render.
    template_name: str

    # The context dictionary with which to render the template.
    template_context: dict | None = None

    def get_template_name(self) -> str:
        """
        Get the Flask template name to render.
        """

        return self.template_name

    def _get_template_name(self) -> str:
        """
        Internally get the Flask template name to render.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        return self.get_template_name()

    def get_template_context(self) -> dict | None:
        """
        Get the context dictionary to render the template.
        """

        return self.template_context

    def _get_template_context(self) -> dict | None:
        """
        Internally get the context dictionary to render the template.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        return self.get_template_context()


class TemplateView(TemplateViewMixin, flask.views.View):
    """
    A view that renders a template with context.
    """

    def dispatch_request(self: TemplateViewMixin, **kwargs):
        """
        Render the template with the template context.
        """

        template_name = self._get_template_name()

        if template_context := self._get_template_context():
            return flask.render_template(template_name, **template_context)

        return flask.render_template(template_name)
