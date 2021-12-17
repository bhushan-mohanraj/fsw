"""
A view to redirect to another URL.
"""

import flask
from flask import views


class RedirectView(views.View):
    """
    A view to redirect to another URL.
    """

    redirect_url: str

    def get_redirect_url(self):
        """
        Get the redirect URL.
        """

        return self.redirect_url

    def dispatch_request(self, **kwargs):
        """
        Redirect to the given URL.
        """

        redirect_url = self.get_redirect_url()

        if not redirect_url:
            return flask.abort(404)

        return flask.redirect(redirect_url)
