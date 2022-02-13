"""
A view class to render and process forms.
"""

import flask.views

from fsw.views.redirect import RedirectView
from fsw.views.template import TemplateView


class FormView(TemplateView, RedirectView, flask.views.View):
    """
    A view class to render and process forms.
    """
