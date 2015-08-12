from sleepypuppy import db, app
from sleepypuppy.admin.models import taxonomy
from flask import render_template_string


class Javascript(db.Model):
    """
    Javascript model contains the following parameters:

    name = name of javascriopt file.
    code = code that will be executed when a sleepy puppy payload is executed
    notes = notes

    Javascript is many to many with payload.
    """
    __tablename__ = 'javascript'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    code = db.Column(db.Text(), nullable=False)
    notes = db.Column(db.String(500))
    payloads = db.relationship("Payload", backref='javascript', secondary=taxonomy)

    def show_javascript_ids(self):
        """
        Print javascripts as a list of javascript ids.
        """
        return [i.id for i in self.javascripts]

    def show_javascript_names(self):
        """
        Print javascripts as a string of javascript ids.
        """
        return ','.join(
            [i.name for i in self.javascripts]
        )

    def as_dict(self, payload_id=1):
        """Return Assessment model as JSON object"""
        # render_template_string
        js_dict = {}
        js_dict['name'] = self.name
        js_dict['code'] = render_template_string(self.code,
                                                 hostname=app.config['CALLBACK_HOSTNAME'],
                                                 callback_protocol=app.config.get('CALLBACK_PROTOCOL', 'https'),
                                                 payload_id=payload_id)
        return js_dict


    def __repr__(self):
        return str(self.name)
