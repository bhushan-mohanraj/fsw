import secrets

import flask
import wtforms.csrf.session


class CSRFProtectFormMixin:
    """
    Add CSRF protection to forms, using the Flask session.
    """

    class Meta:
        csrf = True
        csrf_class = wtforms.csrf.session.SessionCSRF
        csrf_secret = secrets.token_hex()
        csrf_context = flask.session
