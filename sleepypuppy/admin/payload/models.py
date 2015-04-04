from sleepypuppy import db, app


class Payload(db.Model):
    """
    Payload model contains the following parameters:

    payload = payload used in xss injection testing.
    url = url where payload is submitted to
    method = method of request to faciliate xss testing
    paramater = parameter which contains the payload
    notes = notes

    Payload provides primary key to Capture, which stores
    a xss capture.
    """
    __tablename__ = 'payloads'

    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(db.String(500))
    url = db.Column(db.String(500))
    method = db.Column(db.String(12))
    parameter = db.Column(db.String(50))
    notes = db.Column(db.String(200))
    assessment = db.Column(db.Integer, db.ForeignKey('assessments.id'))

    # When payloads are deleted, cascade the delete and remove associated captures
    captures = db.relationship("Capture", cascade="all,delete", backref="payloads")

    def as_dict(self):
        """
        Return JSON API object
        """

        # Replace $1 template with configured hostname
        payload = self.payload.replace("$1", "//{}/c.js?u={}".format(app.config['HOSTNAME'], str(self.id)))

        payload_dict = {
            "id": self.id,
            "assessments": [i.as_dict() for i in self.assessments],
            "payload": payload,
            "url": self.url,
            "method": self.method,
            "parameter": self.parameter,
            "notes": self.notes
        }

        return payload_dict

    def show_assessment_ids(self):
        """
        Print payload assessments as a list of assessment ids.
        """
        return [i.id for i in self.assessments]

    def show_assessment_names(self):
        """
        Print payload assessments as a string of assessment names.
        """
        return ','.join(
            [i.name for i in self.assessments]
        )
