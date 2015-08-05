import os
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.actions import action
from wtforms import validators
from wtforms.fields import SelectField, TextAreaField
from sleepypuppy import app, db
from sleepypuppy.admin.capture.models import Capture
from models import Javascript
from flask.ext import login
from flask_wtf import Form


class JavascriptView(ModelView):
    """
    ModelView override of Flask Admin for JavaScripts.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    form_excluded_columns = ('payloads')

    def __init__(self, session, **kwargs):
        super(JavascriptView, self).__init__(Javascript, session, **kwargs)
