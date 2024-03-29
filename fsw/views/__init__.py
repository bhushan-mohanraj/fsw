"""
Classes and helpers for Flask views.

Most FSW view classes
are built under the assumption
that they are instantiated for each request.
Therefore, the `init_every_request` argument of `View.as_view`
should never be `False` for FSW view classes.
"""

from fsw.views.forms import FormView as FormView
from fsw.views.models import CreateModelView as CreateModelView
from fsw.views.models import DeleteModelView as DeleteModelView
from fsw.views.models import ReadModelView as ReadModelView
from fsw.views.models import ReadOneModelView as ReadOneModelView
from fsw.views.models import UpdateModelView as UpdateModelView
from fsw.views.redirects import RedirectView as RedirectView
from fsw.views.templates import TemplateView as TemplateView
