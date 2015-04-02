import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = os.getenv('secret_key', 'ThiSISMYDARKSECRET!@#')

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.getenv('csrf_session_key', 'ThiSISMYDARKSECRET!@#')

SQLALCHEMY_DATABASE_URI = os.getenv('sleepypuppy_db', 'sqlite:////tmp/sleepy-db.db')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

LOG_LEVEL = "DEBUG"
LOG_FILE = "sleepypuppy.log"

HOSTNAME = 'crushit.today'

# Email server configuration
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_SENDER = 'root@your-domain.com'
#MAIL_USE_TLS = False
#MAIL_USE_SSL = False
#MAIL_USERNAME = 'you'
#MAIL_PASSWORD = 'your-password'
