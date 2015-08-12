from flask.ext.admin.contrib.sqla import ModelView
from models import Javascript
from sleepypuppy.admin.payload.models import Payload
from flask.ext import login
from flask_wtf import Form
from sleepypuppy import db


class JavascriptView(ModelView):
    """
    ModelView override of Flask Admin for JavaScripts.
    """
    # CSRF protection
    form_base_class = Form

    # Ensure user is authenticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    # No need to show the many/many relationship for payloads
    form_excluded_columns = ('payloads')

    # Excluding code from view
    column_exclude_list = ('code')

    # Flask create template
    #create_template = 'create_javascript_template.html'

    def on_model_delete(self, model):
        # TODO: does this work?
        payloads = Payload.query.all()
        print payloads
        for payload in payloads:

            if payload.ordering is not None:
                print "count: {}".format(payload.ordering)
                payload.ordering = payload.ordering.replace(str(model.id) + ",", "")
                payload.ordering = payload.ordering.replace("," + str(model.id), "")
                payload.ordering = payload.ordering.replace(str(model.id), "")
                db.session.add(payload)
                db.session.commit()

    def __init__(self, session, **kwargs):
        super(JavascriptView, self).__init__(Javascript, session, **kwargs)
