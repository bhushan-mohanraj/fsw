import secrets

from flask import session
from wtforms.csrf.session import SessionCSRF


class CSRFMixin:
    """
    Add CSRF protection to forms, using the Flask session.
    """

    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = secrets.token_hex()
        csrf_context = session
