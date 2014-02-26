from sleepypuppy import db,app

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
    assessment =  db.Column(db.Integer, db.ForeignKey('assessments.id'))
    # When payloads are deleted, cascade the delete and remove associated captures
    captures = db.relationship("Capture", cascade="all,delete", backref="payloads")

    def as_dict(self):
        """
        Return JSON API object
        """
        payload_dict = {}
        assessment_names = []
        for i in self.assessments:
            assessment_names.append(i.as_dict())
        payload_dict["id"] = self.id
        payload_dict["assessments"] = assessment_names
        # Replace $1 template with configured hostname
        payload_dict["payload"] = self.payload.replace("$1","//" + app.config['HOSTNAME'] + "/c.js?u=" + str(self.id))
        payload_dict["url"] = self.url
        payload_dict["method"] = self.method
        payload_dict["parameter"] = self.parameter
        payload_dict["notes"] = self.notes

        return payload_dict

    def show_assessment_ids(self):
        """
        Print payload assessments as a list of assessment ids.
        """
        assessment_names = []
        for i in self.assessments:
            assessment_names.append(i.id)
        return assessment_names

    def show_assessment_names(self):
        """
        Print payload assessments as a string of assessment names.
        """
        assessment_names = []
        for i in self.assessments:
            assessment_names.append(i.name)
        return ','.join(assessment_names)
