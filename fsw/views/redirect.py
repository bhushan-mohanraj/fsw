"""
A view to redirect to another URL.
"""

import flask
import flask.views


class RedirectViewMixin:
    """
    A mixin for views the redirect to another URL.
    """

    # The URL to redirect to. For Flask views, use `flask.url_for`.
    redirect_url: str | None

    def get_redirect_url(self) -> str | None:
        """
        Get the redirect URL.
        """

        return self.redirect_url

    def _get_redirect_url(self) -> str | None:
        """
        Internally get the redirect URL.

        Base subclasses can implement this method with custom behavior
        run before or after behavior implemented by view subclasses.

        If this method returns a Falsy value, the view returns a 404 error.
        """

        return self.get_redirect_url()


class RedirectView(flask.views.View, RedirectViewMixin):
    """
    A view that redirects to another URL.
    """

    def dispatch_request(self, **kwargs):
        """
        Redirect to the given URL.
        """

        if redirect_url := self._get_redirect_url():
            return flask.redirect(redirect_url)

        return flask.abort(404)
