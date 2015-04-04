from sleepypuppy import db
from sqlalchemy.orm import relationship
from sleepypuppy.admin.models import user_associations
from sleepypuppy.admin.assessment.models import Assessment


class User(db.Model):
    """
    User model contains the following parameters used for email notifications:

    email = email address to send capture notifications to.
    assessments = list of assessments the email address will recieve captures for.

    Has an association of assessments with users.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    assessments = relationship(Assessment, secondary=user_associations, backref="users")

    def __repr__(self):
        return self.email
