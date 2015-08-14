from flask.ext.admin.contrib.sqla import ModelView
from models import GenericCollector
from sleepypuppy.admin.payload.models import Payload
from flask.ext import login
from flask_wtf import Form


class GenericCollectorView(ModelView):
    """
    ModelView override of Flask Admin for JavaScripts.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    # No need to show the many/many relationship for payloads

    can_create = False
    can_edit = False

    list_template = 'generic_list.html'
    column_list = (
        'pub_date',
        'payload',
        'assessment',
        'javascript_name',
        'url',
        'referrer',
        'data'
    )
    column_filters = ('id', 'payload', 'javascript_name', 'url', 'referrer')

    column_sortable_list = (
        'pub_date',
        'payload',
        'javascript_name',
        'url',
        'referrer'
    )

    column_formatters = dict(
        payload=lambda v, c, m, p: str(m.payloads)
        if m.payloads is not None else "Payload Not Found",
        assessment=lambda v, c, m, p: str(
            Payload.query.filter_by(id=m.payloads.id)
            .first()
            .assessments
            if Payload.query.filter_by(id=m.payloads.id).first() is not None
            else "Not Found"
        ).strip('[]')
    )

    def __init__(self, session, **kwargs):
        super(GenericCollectorView, self).__init__(GenericCollector, session, **kwargs)
