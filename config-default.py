import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False

SECRET_KEY = os.getenv('secret_key', 'ThiSISMYDARKSECRET!@#')

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.getenv('csrf_session_key', 'ThiSISMYDARKSECRET!@#')

SQLALCHEMY_DATABASE_URI = os.getenv('sleepypuppy_db', 'sqlite:////tmp/sleepy-db.db')

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
UPLOAD_SCREENSHOTS_TO_S3 = False
S3_BUCKET = ""
S3_FILES_PREFIX = "sleepypuppy"

LOG_LEVEL = "DEBUG"
LOG_FILE = "sleepypuppy.log"

HOSTNAME = 'localhost' # for getting the JS file.
CALLBACK_HOSTNAME = HOSTNAME
CALLBACK_PROTOCOL = 'http' # http for local dev, https for deploy

# Email server configuration
# SES Options:
EMAILS_USE_SES = False
SES_REGION = 'us-east-1'

# SMTP Options:
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_SENDER =  os.getenv('sender', 'sleepypuppy@domain.com')
#MAIL_USE_TLS = False
#MAIL_USE_SSL = False
#MAIL_USERNAME = 'you'
#MAIL_PASSWORD = 'your-password'

ALLOWED_DOMAINS = ['localhost']
