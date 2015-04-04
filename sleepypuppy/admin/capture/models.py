from sleepypuppy import db
import datetime


class Capture(db.Model):
    """
    Capture model contains the following parameters:

    assessment = assessment name(s) assocaited with capture
    url = url where cross-site scripting was triggered
    referrer = referrer string of request
    cookies = any cookies not containing the HttpOnly flag from request
    user_agent = user-agent string
    payload = to be removed
    screenshot = screenshot identifier
    pub_date = Date with which the capature was recieved
    """
    __tablename__ = 'captures'

    id = db.Column(db.Integer, primary_key=True)
    assessment = db.Column(db.String(200))
    url = db.Column(db.String(2000), unique=False)
    referrer = db.Column(db.String(2000), unique=False)
    cookies = db.Column(db.String(2000), unique=False)
    user_agent = db.Column(db.String(512), unique=False)
    payload = db.Column(db.Integer)
    screenshot = db.Column(db.String(20), unique=False)
    pub_date = db.Column(db.String(512), unique=False)
    dom = db.Column(db.String(65535), unique=False)
    payload_id = db.Column(db.Integer, db.ForeignKey('payloads.id'))

    def as_dict(self):
        """Return Capture model as JSON object"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __init__(self, assessment, url, referrer, cookies, user_agent,
                 payload, screenshot, dom, pub_date=None):
        self.assessment = assessment
        self.url = url
        self.referrer = referrer
        self.cookies = cookies
        self.user_agent = user_agent
        self.payload = payload
        self.screenshot = screenshot
        self.dom = dom
        self.payload_id = payload
        # Set datetime when a capture is recieved
        if pub_date is None:
            pub_date = str(datetime.datetime.now())
        self.pub_date = pub_date

    def __repr__(self):
        return '<Uri %r>' % self.url
