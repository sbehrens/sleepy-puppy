from sleepypuppy import db
from sleepypuppy.admin.models import assessment_associations


class Assessment(db.Model):
    """
    Assessemt model contains the following parameters:

    name = name of the assessment you are working on.
    payloads = payloads assocaited with the assessment
    """
    __tablename__ = 'assessments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    payloads = db.relationship("Payload", secondary=assessment_associations, backref="assessments")

    def as_dict(self):
        """Return Assessment model as JSON object"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return str(self.name)
