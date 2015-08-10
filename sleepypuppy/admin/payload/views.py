import os
from sleepypuppy import app, db
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.actions import action
from wtforms import validators
from wtforms.fields import SelectField, TextAreaField, SelectMultipleField
from wtforms.widgets import TextInput
from flask.ext.admin._compat import text_type
from sleepypuppy.admin.javascript.models import Javascript
from sleepypuppy.admin.capture.models import Capture
from models import Payload
from flask.ext import login
from flask_wtf import Form


class Select2MultipleWidget(TextInput):
    """
    (...)

    By default, the `_value()` method will be called upon the associated field
    to provide the ``value=`` HTML attribute.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-choices', self.json_choices(field))
        return super(Select2MultipleWidget, self).__call__(field, **kwargs)

    @staticmethod
    def json_choices(field):
        objects = ('{{"id": {}, "text": "{}"}}'.format(*c) for c in field.iter_choices())
        print 'i am here'
        return '[' + ','.join(objects) + ']'


class Select2MultipleField(SelectMultipleField):
    """
        `Select2 <https://github.com/ivaynberg/select2>`_ styled select widget.

        You must include select2.js, form.js and select2 stylesheet for it to
        work.

        This is a slightly altered derivation of the original Select2Field.
    """
    widget = Select2MultipleWidget()

    def __init__(self, label=None, validators=None, coerce=text_type,
                 choices=None, allow_blank=False, blank_text=None, **kwargs):
        super(Select2MultipleField, self).__init__(
            label, validators, coerce, choices, **kwargs
        )
        self.allow_blank = allow_blank
        self.blank_text = blank_text or ' '
        self.choices = db.session.query(Javascript.id, Javascript.name).all()

    def iter_choices(self):
        # moved the query here so it updates
        choices = db.session.query(Javascript.id, Javascript.name).all()
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is [])

        for value, label in choices:
            yield (value, label, self.coerce(value) in self.data)

    def process_data(self, value):
        if not value:
            self.data = []
        else:
            try:
                self.data = []
                for v in value:
                    self.data.append(self.coerce(v[0]))
            except (ValueError, TypeError):
                self.data = []

    def process_formdata(self, valuelist):
        if valuelist:
            if valuelist[0] == '__None':
                self.data = []
            else:
                try:
                    self.data = []
                    for value in valuelist[0].split(','):
                        print value
                        self.data.append(self.coerce(value))
                except ValueError:
                    raise ValueError(self.gettext(u'Invalid: could not coerce {}'.format(value)))

    def pre_validate(self, form):
        if self.allow_blank and self.data is []:
            return

        super(Select2MultipleField, self).pre_validate(form)

    def _value(self):
        return ','.join(map(str, self.data))


class PayloadView(ModelView):
    """
    ModelView override of Flask Admin for Payloads.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    def on_form_prefill(self, form, id):
        # help order things in the right way.
        to_process = self.session.query(Payload.ordering).filter(Payload.id == id).first()
        if to_process[0]:
            form.javascript_list.process_data(to_process[0].split(','))

    # Custom templates for listing models
    list_template = 'payload_list.html'

    hostname = app.config['HOSTNAME']

    def on_model_change(self, form, model, is_created=False):
        model.ordering = ','.join(str(v) for v in form.javascript_list.data)
        print model.ordering
        print 'on_model_change'
        db.session.add(model)
        db.session.commit()

    # Method to cascade delete screenshots when removing a payload
    def delete_screenshots(self, model):
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
        'snooze',
        'run_once',
        'javascripts',
        'notes'
    )

    column_sortable_list = (
        'id',
        'assessments',
        # 'captured',
        'payload',
        'url',
        'method',
        'parameter'
    )

    column_filters = (
        'id',
        'assessments',
        'payload',
        'url',
        'method',
        'parameter'
    )

    form_excluded_columns = ('captures', 'uid')
    form_columns = ('javascript_list',
                    'payload',
                    'url',
                    'method',
                    'parameter',
                    'notes',
                    'snooze',
                    'run_once',
                    'assessments')

    # Check if payload has associated captures, and format column if found
    # Format payload string to include hostname
    column_formatters = dict(
        javascripts=lambda v, c, m, p: [Javascript.query.filter_by(id=thing).first() for thing in Payload.query.filter_by(id=m.id).first().ordering.split(',')]
        if Payload.query.filter_by(id=m.id).first().ordering is not None or "" else "Default",
        captured=lambda v, c, m, p: Capture.query.filter_by(payload_id=m.id).first().id
        if Capture.query.filter_by(payload_id=m.id).first() is not None else "None",
        payload=lambda v, c, m, p: m.payload.replace("$1",
                                                     "//{}/x?u={}".format(app.config['HOSTNAME'], str(m.id)))
    )

    # Extra fields
    # 'javascript_list' name chosen to avoid name conflict
    form_extra_fields = {
        'javascript_list': Select2MultipleField(
            'Javascripts',
            coerce=int),
    }

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
        snooze=dict(
            description="Stop captures for this payload"
        ),
        run_once=dict(
            description="Only run capture once for this payload"
        ),
        assessment=dict(
            validators=[validators.required()]
        ),
        javascript_list=dict(
            description="Stuff.",
            label="Javascripts",
            validators=[validators.required()]
        )
    )

    def __init__(self, session, **kwargs):
        super(PayloadView, self).__init__(Payload, session, **kwargs)
