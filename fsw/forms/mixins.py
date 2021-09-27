import os
from flask import session
from wtforms.csrf.session import SessionCSRF


class CSRFMixin:
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = os.urandom(32)
        csrf_context = session
