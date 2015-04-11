from sleepypuppy import db, bcrypt
from sqlalchemy import event
from os import urandom


class Admin(db.Model):
    """
    Admin model contols how users autheticate to Sleepy Puppy
    The model also automatically generates API keys for administrators.

    login = account for authetication
    password = self explanatory
    api_key = 40 character urandom hex encoded string
    """

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80))
    password = db.Column(db.String(64))
    api_key = db.Column(db.String(80))

    # Integrate Admin model with Flask Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __init__(self, login="", password=""):
        self.login = login
        self.password = password
        self.api_key = urandom(40).encode('hex')

    # Required for administrative interface
    def __unicode__(self):
        return self.username


# Make sure to encrypt passwords before create and updates
@event.listens_for(Admin, 'before_insert')
def receive_before_insert(mapper, connection, target):
    target.password = bcrypt.generate_password_hash(target.password)
    target.api_key = urandom(40).encode('hex')


@event.listens_for(Admin, 'before_update')
def receive_before_update(mapper, connection, target):
    target.password = bcrypt.generate_password_hash(target.password)
    target.api_key = urandom(40).encode('hex')
