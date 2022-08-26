"""
A view to redirect to another URL.
"""

import flask
import flask.views


class RedirectView(flask.views.View):
    """
    A view that redirects to a URL.
    """

    # The URL to redirect to. For views, use `flask.url_for`.
    redirect_url: str

    def get_redirect_url(self) -> str:
        """
        Get the redirect URL.
        """
        return self.redirect_url

    def dispatch_request(self, **kwargs):
        """
        Redirect to the given URL.
        """
        redirect_url = self.get_redirect_url()

        return flask.redirect(redirect_url)
