import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SSL = True

# Security configuration settings
SECRET_KEY = os.getenv('secret_key', 'ThiSISMYDARKSECRET!@#')
CSRF_ENABLED = True
CSRF_SESSION_KEY = os.getenv('csrf_session_key', 'ThiSISMYDARKSECRET!@#')

# Database configuration settings
SQLALCHEMY_DATABASE_URI = os.getenv('sleepypuppy_db', 'sqlite:////tmp/sleepy-db.db')

# Screenshot storage configuration settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ASSETS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sleepypuppy/assets')
print ASSETS_FOLDER
UPLOAD_SCREENSHOTS_TO_S3 = False
S3_BUCKET = ""
S3_FILES_PREFIX = "sleepypuppy"

# Log configuration settings
LOG_LEVEL = "DEBUG"
LOG_FILE = "sleepypuppy.log"

# Callback configuration settings for JS captures
HOSTNAME = '127.0.0.1:8000'
# for getting the JS file.
CALLBACK_HOSTNAME = HOSTNAME
# http for local dev, https for deploy
CALLBACK_PROTOCOL = 'http'

# Email server configuration
# SES Options:
EMAILS_USE_SES = True
SES_REGION = 'us-east-1'

# SMTP Options:
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_SENDER = os.getenv('sender', 'monterey@saasmail.netflix.com')
# Uncomment if your SMTP server requires authentication
# MAIL_USE_TLS = False
# MAIL_USE_SSL = False
# MAIL_USERNAME = 'you'
# MAIL_PASSWORD = 'your-password'

# Captures will only be logged from the following list of domains
# By default, it will allow all domains if list is empty
ALLOWED_DOMAINS = []
