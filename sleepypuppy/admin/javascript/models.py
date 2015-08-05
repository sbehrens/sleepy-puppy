from sleepypuppy import db, app
from sleepypuppy.admin.models import taxonomy

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
    payloads = db.relationship('Payload', backref='javascript', secondary=taxonomy)

    # When payloads are deleted, cascade the delete and remove associated captures

    # def as_dict(self):
    #     """
    #     Return JSON API object
    #     """

    #     # Replace $1 template with configured hostname
    #     payload = self.payload.replace("$1", "//{}/x?u={}".format(app.config['HOSTNAME'], str(self.id)))

    #     payload_dict = {
    #         "id": self.id,
    #         "assessments": [i.as_dict() for i in self.assessments],
    #         "javascripts": [i.as_dict() for i in self.javascripts],
    #         "payload": payload,
    #         "url": self.url,
    #         "method": self.method,
    #         "parameter": self.parameter,
    #         "run_once": self.run_once,
    #         "snooze": self.snooze,
    #         "notes": self.notes
    #     }

    #     return payload_dict

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
        
    def __repr__(self):
        return str(self.name)
