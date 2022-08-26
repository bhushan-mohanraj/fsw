"""
A mixin that adds CSRF protection to WTForms forms.
"""

import flask
import wtforms.csrf.session


class CSRFProtectFormMixin:
    """
    A mixin that adds CSRF protection to forms if the Flask app context exists,
    using the WTForms implementation of CSRF protection and the Flask session.

    This mixin sets the CSRF secret key to the Flask application secret key.
    """

    if flask.current_app:
        # Defining the `Meta` class in a mixin
        # does not override values set by other definitions.
        class Meta:
            """
            A class that enables CSRF protection,
            using the default WTForms implementation.
            """

            csrf = True
            csrf_class = wtforms.csrf.session.SessionCSRF
            csrf_secret = flask.current_app.secret_key
            csrf_context = flask.session
