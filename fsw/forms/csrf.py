"""
A mixin that adds CSRF protection to WTForms forms.
"""

import secrets

import flask
import wtforms.csrf.session


class CSRFProtectFormMixin:
    """
    A mixin that adds CSRF protection to forms if the Flask app context exists,
    using the WTForms implementation of CSRF protection and the Flask session.
    """

    if flask.current_app:
        class Meta:
            """
            A class that enables CSRF protection,
            using the default WTForms implementation.
            """

            csrf = True
            csrf_class = wtforms.csrf.session.SessionCSRF
            csrf_secret = secrets.token_hex()
            csrf_context = flask.session
