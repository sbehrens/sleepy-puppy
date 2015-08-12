from flask.ext.admin.contrib.sqla import ModelView
from wtforms.fields import SelectField, TextAreaField
from sleepypuppy.admin.payload.models import Payload
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

    column_filters = ('id', 'ip_address', 'user_agent', 'referrer')

    # Disable unnneeded CRUD operations
    can_create = False
    can_edit = False

    # Make form use dropdown boxes, default text, required form elements
    form_overrides = dict(
        method=SelectField,
        notes=TextAreaField
    )

    # Column list
    column_list = (
        'pub_date',
        'assessment',
        'referrer',
        'user_agent',
        'ip_address'
    )

    # Format the data in these columns
    column_formatters = dict(
        assessment=lambda v, c, m, p: str(
            Payload.query.filter_by(id=m.payload_id)
            .first()
            .assessments
            if Payload.query.filter_by(id=m.payload_id).first() is not None
            else "Not Found"
        ).strip('[]')
    )

    def __init__(self, session, **kwargs):
        super(AccessLogView, self).__init__(AccessLog, session, **kwargs)
