"""
A view to render a template with context.
"""

import flask
import flask.views


class TemplateView(flask.views.View):
    """
    A view that renders a template with context.
    """

    # The Flask template name to render.
    template_name: str

    # The context dictionary with which to render the template.
    template_context: dict = {}

    def get_template_name(self) -> str:
        """
        Get the Flask template name to render.
        """

        return self.template_name

    def get_template_context(self) -> dict:
        """
        Get the context dictionary with which to render the template.
        """

        return self.template_context

    def dispatch_request(self: TemplateViewMixin, **kwargs):
        """
        Render the template with the template context.
        """

        template_name = self.get_template_name()
        template_context = self.get_template_context()

        if not template_context:
            return flask.render_template(template_name)

        return flask.render_template(template_name, **template_context)
