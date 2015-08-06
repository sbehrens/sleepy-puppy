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

    form_excluded_columns = ('payloads')

    def on_model_delete(self,model):
        payloads = Payload.query.all()
        for payload in payloads:
            if payload.ordering is not None:
                payload.ordering = payload.ordering.replace(str(model.id) + ",", "")
                payload.ordering = payload.ordering.replace("," + str(model.id), "") 
                payload.ordering = payload.ordering.replace(str(model.id), "") 
                db.session.add(payload)
                db.session.commit()

    def __init__(self, session, **kwargs):
        super(JavascriptView, self).__init__(Javascript, session, **kwargs)
