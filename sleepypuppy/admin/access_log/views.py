import os
from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField, TextAreaField
from sleepypuppy import app, db
from sleepypuppy.admin.capture.models import Capture
from models import AccessLog
from flask.ext import login
from flask_wtf import Form


class AccessLogView(ModelView):
    """
    ModelView override of Flask Admin for Access Logs.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    form_excluded_columns = ('captures', 'uid')

    # Disable unnneeded CRUD operations
    can_create = False
    can_edit = False
    
    # Make form use dropdown boxes, default text, required form elements
    form_overrides = dict(
        method=SelectField,
        notes=TextAreaField
    )

    def __init__(self, session, **kwargs):
        super(AccessLogView, self).__init__(AccessLog, session, **kwargs)
