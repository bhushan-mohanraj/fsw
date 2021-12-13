"""
A view to redirect to another URL.
"""

import flask
from flask import views


class RedirectView(views.View):
    """
    A view to redirect to another URL.
    """

    redirect_url: str  # The URL to redirect to.

    def dispatch_request(self):
        """
        Redirect to the given URL.
        """

        return flask.redirect(self.redirect_url)
