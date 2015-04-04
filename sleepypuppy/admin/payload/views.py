import os
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.actions import action
from wtforms import validators
from wtforms.fields import SelectField, TextAreaField
from sleepypuppy import app, db
from sleepypuppy.admin.capture.models import Capture
from models import Payload
from flask.ext import login
from flask_wtf import Form


class PayloadView(ModelView):
    """
    ModelView override of Flask Admin for Payloads.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    # Custom templates for listing models and creating models
    create_template = 'payload_create_template.html'
    list_template = 'payload_list_template.html'

    hostname = app.config['HOSTNAME']

    # Method to cascade delete screenshots when removing a payload
    @staticmethod
    def delete_screenshots(model):
        cascaded_captures = Capture.query.filter_by(payload_id=model.id).all()
        for capture in cascaded_captures:
            try:
                os.remove("uploads/{}.png".format(capture.screenshot))
                os.remove("uploads/small_{}.png".format(capture.screenshot))
            except:
                pass
    on_model_delete = delete_screenshots

    @action('delete', 'Delete', 'Are you sure you want to delete?')
    def action_delete(self, items):
        for record in items:
            cascaded_captures = Capture.query.filter_by(payload_id=record).all()
            for capture in cascaded_captures:
                try:
                    os.remove("uploads/{}.png".format(capture.screenshot))
                    os.remove("uploads/small_{}.png".format(capture.screenshot))
                except:
                    pass
            page = Payload.query.get(record)
            db.session.delete(page)
            db.session.commit()

    # Column tweaks
    column_list = (
        'id',
        'assessments',
        'captured',
        'payload',
        'url',
        'method',
        'parameter',
        'notes'
    )

    column_sortable_list = (
        'id',
        'assessments',
        'captured',
        'payload',
        'url',
        'method',
        'parameter'
    )

    column_filters = (
        'id',
        'assessment',
        'payload',
        'url',
        'method',
        'parameter'
    )

    form_excluded_columns = ('captures', 'uid')

    # Check if payload has associated captures, and format column if found
    # Format payload string to include hostname
    column_formatters = dict(
        captured=lambda v, c, m, p: Capture.query.filter_by(payload_id=m.id).first().id
        if Capture.query.filter_by(payload_id=m.id).first() is not None else "None",
        payload=lambda v, c, m, p: m.payload.replace("$1", "//{}/c.js?u={}".format(app.config['HOSTNAME'], str(m.id)))
    )

    # Make form use dropdown boxes, default text, required form elements
    form_overrides = dict(
        method=SelectField,
        notes=TextAreaField
    )

    form_args = dict(
        method=dict(
            choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')]
        ),
        payload=dict(
            description="Use $1 as a placeholder for the Javascript URL.",
            default="<script src=$1></script>",
            validators=[validators.required()]
        ),
        assessment=dict(
            validators=[validators.required()]
        )
    )

    def __init__(self, session, **kwargs):
        super(PayloadView, self).__init__(Payload, session, **kwargs)
