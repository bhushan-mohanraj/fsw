"""
A view to redirect to another URL.
"""

import flask
import flask.views


class RedirectViewMixin:
    """
    A mixin for views the redirect to another URL.
    """

    # The URL to redirect to. For views, use `flask.url_for`.
    redirect_url: str

    def get_redirect_url(self) -> str:
        """
        Get the redirect URL.

        This method overrides the `redirect_url` attribute.
        """

        return self.redirect_url

    def _get_redirect_url(self) -> str:
        """
        Internally get the redirect URL.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.
        """

        return self.get_redirect_url()


class RedirectView(RedirectViewMixin, flask.views.View):
    """
    A view that redirects to another URL.
    """

    def dispatch_request(self: RedirectViewMixin, **kwargs):
        """
        Redirect to the given URL.
        """

        redirect_url = self._get_redirect_url()

        return flask.redirect(redirect_url)
