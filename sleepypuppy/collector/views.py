import urllib
from flask import request
from flask import render_template
from flask_mail import Message
from sleepypuppy import app, db, flask_mail, csrf_protect
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.user.models import User

@app.route('/c.js', methods=['GET'])
def collector(xss_uid = 1):
    """
    Render Javascript payload with unique identifier and hosts for callback.
    """
    xss_uid = request.args.get('u')
    return render_template('c.js', xss_uid=xss_uid, hostname=app.config['HOSTNAME'])

def email_subscriptions(xss_uid, url):
    """
    Email all users who are subscribed to assessments.
    """
    email_list = []
    notify_jobs = Payload.query.filter_by(id=xss_uid).first()
    user_notify = User.query.all()
    # Loop through every User and intersect if the capture is associated with
    # an assessment they are subscribed to recieve notificaitons for.
    for i in xrange(len(user_notify)):
        user_subscriptions = []
        for e in user_notify[i].assessments:
            user_subscriptions.append(e.id)
        if len(set(notify_jobs.show_assessment_ids()).intersection(user_subscriptions)) > 0:
            email_list.append(user_notify[i].email)
    print 'foo'
    print email_list
    # If there are people to email, email them that a capture was recieved
    if email_list:
        msg = Message("[Sleepy Puppy] - Capture Recieved From: " + url,
            sender=app.config['MAIL_SENDER'],
            recipients=email_list)
        msg.html = "<b>Associated Assessments: <b>" + notify_jobs.show_assessment_names() + "<br><br>"
        flask_mail.send(msg)

# Disable CSRF protection on callback posts
@csrf_protect.exempt
@app.route('/callbacks', methods = ['POST'])
def getCallbacks():
    """
    Method to handle Capture creation.
    """
    if request.method == 'POST':
        url = urllib.unquote(str(request.form['uri']))
        referrer = urllib.unquote(str(request.form['referrer']))
        cookies = urllib.unquote(str(request.form['cookies']))
        user_agent = urllib.unquote(str(request.form['user_agent']))
        assessment = Payload.query.filter_by(id=int(request.form['xss_uid'])).first()
        xss_uid = Payload.query.filter_by(id=int(request.form['xss_uid'])).first()
        screenshot = int(request.form['screenshot'])
        dom = urllib.unquote(str(request.form['dom']))

        # If it's a rogue capture, log it anyway.
        if assessment == None:
            client_info = Capture("Not found", url, referrer, cookies, user_agent, "Not found", screenshot, dom)
        else:
            # Create the capture with associated assessment/payload
            client_info = Capture(assessment.id, url, referrer, cookies, user_agent, xss_uid.id, screenshot, dom)
            email_subscriptions(xss_uid.id, url)

        db.session.add(client_info)
        db.session.commit()
        return ""
