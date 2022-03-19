"""
A view to redirect to another URL.
"""

import flask
import flask.views


class RedirectView(flask.views.View):
    """
    A view to redirect to another URL.
    """

    redirect_url: str = ""

    def get_redirect_url(self) -> str:
        """
        Get the redirect URL.
        """

        return self.redirect_url

    def _get_redirect_url(self) -> str:
        """
        Internally get the redirect URL.

        Base subclasses can implement this method with custom behavior
        that runs before or after behavior implemented by view subclasses.
        """

        return self.get_redirect_url()

    def dispatch_request(self, **kwargs):
        """
        Redirect to the given URL.
        """

        redirect_url = self._get_redirect_url()

        return flask.redirect(redirect_url)
