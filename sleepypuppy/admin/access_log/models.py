from sleepypuppy import db, bcrypt
from sqlalchemy import event
from os import urandom
import datetime


class AccessLog(db.Model):
    """
    Access Log records GET requests to payloads.  This can be helpful
    for payloads that are not executing due to namespace conflicts, client
    side controls, or other unexpected issues.  


    """

    id = db.Column(db.Integer, primary_key=True)
    payload_id = db.Column(db.Integer)
    pub_date = db.Column(db.String(512), unique=False)
    referrer = db.Column(db.String(1024))
    user_agent = db.Column(db.String(512))
    ip_address = db.Column(db.String(80))

    def __init__(self, payload_id, referrer, user_agent, ip_address, pub_date=None):
        self.payload_id = payload_id
        self.referrer = referrer
        self.user_agent = user_agent
        self.ip_address = ip_address
        if pub_date is None:
            pub_date = str(datetime.datetime.now())
        self.pub_date = pub_date

    

    def as_dict(self):
        """Return Access Log model as JSON object"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

