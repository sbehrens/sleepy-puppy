from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask, redirect, request, abort
from flask.ext import login
from flask.ext.bcrypt import Bcrypt
from flask.ext.restful import Api
from flask.ext.admin import Admin
from flask.ext.mail import Mail
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import flask_wtf

# Config and App setups
app = Flask(__name__)
app.config.from_object('config-default')
app.debug = app.config.get('DEBUG')
# Log handler functionality
handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000000, backupCount=100)
handler.setFormatter(
    Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
)
handler.setLevel(app.config.get('LOG_LEVEL'))
app.logger.addHandler(handler)

# CSRF Protection
csrf_protect = flask_wtf.CsrfProtect(app)

# Initalize DB object
db = SQLAlchemy(app)

# Initalize Bcrypt object for password hashing
bcrypt = Bcrypt(app)

# Initalize flask mail object for email notifications
flask_mail = Mail(app)

# Decorator for Token Auth on API Requests
from sleepypuppy.admin.admin.models import Admin as AdminModel


# The dectorat function for API token auth
def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get('Token'):
            for keys in AdminModel.query.all():
                print keys.api_key
                if request.headers.get('Token') == keys.api_key:
                    return view_function(*args, **kwargs)
            abort(401)
        else:
            abort(401)
    return decorated_function

# Initalize the Flask API
flask_api = Api(app, decorators=[csrf_protect.exempt, require_appkey])


# Initalize Flask Login functionality
def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(AdminModel).get(user_id)

# Intalize the login manager for sleepy puppy
init_login()

# Create the Flask Admin object
from admin.admin.views import MyAdminIndexView, AdminView
flask_admin = Admin(app, 'Sleepy Puppy', index_view=MyAdminIndexView(), base_template='admin/base.html')

# Import the collector which is used to collect capture information
from collector import views

# Import the screenshot upload handler
from upload import upload

# Initalize all Flask API views
from api.views import CaptureView, CaptureViewList, PayloadView, PayloadViewList, AssessmentView, AssessmentViewList
flask_api.add_resource(AssessmentViewList, '/api/assessments')
flask_api.add_resource(AssessmentView, '/api/assessments/<int:id>')
flask_api.add_resource(CaptureViewList, '/api/captures')
flask_api.add_resource(CaptureView, '/api/captures/<int:id>')
flask_api.add_resource(PayloadViewList, '/api/payloads')
flask_api.add_resource(PayloadView, '/api/payloads/<int:id>')

# Initalize all Flask Admin dashboard views
from admin.capture.views import CaptureView
from admin.payload.views import PayloadView
from admin.user.views import UserView
from admin.assessment.views import AssessmentView

# Add all Flask Admin routes
flask_admin.add_view(PayloadView(db.session))
flask_admin.add_view(CaptureView(db.session))
flask_admin.add_view(UserView(db.session))
flask_admin.add_view(AssessmentView(db.session))
flask_admin.add_view(AdminView(AdminModel, db.session))
from admin import views

# Default route redirect to admin page
@app.route('/')
def index():
    return redirect('/admin', 302)

