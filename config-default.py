import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True


SECRET_KEY = "thisIs_soS_ecret_shh!!don'ttell"

CSRF_ENABLED = True
CSRF_SESSION_KEY = "thisistheawes0mestkeytohaveever!!!"

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/2sleepypuppy.db'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

LOG_LEVEL = "DEBUG"
LOG_FILE = "sleepypuppy.log"

HOSTNAME = 'crushit.today'

# Email server configuration
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_SENDER = 'sbehrens@netflix.com'
#MAIL_USE_TLS = False
#MAIL_USE_SSL = False
#MAIL_USERNAME = 'you'
#MAIL_PASSWORD = 'your-password'
