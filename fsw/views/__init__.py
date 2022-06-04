"""
Classes and helpers for Flask views.
"""

__all__ = [
    "RedirectView",
    "TemplateView",
    "FormView",
    "ReadModelView",
    "ReadOneModelView",
    "CreateModelView",
    "UpdateModelView",
    "DeleteModelView",
]

from fsw.views.redirects import RedirectView
from fsw.views.templates import TemplateView
from fsw.views.forms import FormView
from fsw.views.models import ReadModelView
from fsw.views.models import ReadOneModelView
from fsw.views.models import CreateModelView
from fsw.views.models import UpdateModelView
from fsw.views.models import DeleteModelView
