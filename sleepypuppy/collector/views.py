import urllib
from flask import request
from flask import render_template
from flask_mail import Message
from sleepypuppy import app, db, flask_mail, csrf_protect
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.user.models import User
from flask import Response
from urlparse import urlparse

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
    try:
        the_payload = Payload.query.filter_by(id=int(xss_uid)).first()
        if the_payload.snooze:
            return ''
        if the_payload.run_once and Capture.query.filter_by(payload_id=int(xss_uid)).first():
            return ''
    except:
        pass 

    # Default render tempalte, may need to modify based on new JS ideas
    
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

    import cgi
    subject = "[Sleepy Puppy] - Capture Recieved From: {}".format(
        cgi.escape(url, quote=True)
    )
    html = "<b>Associated Assessments: </b>{}<br/>".format(
        cgi.escape(notify_jobs.show_assessment_names(), quote=True)
    )
    html += "<b>URL: </b>{}<br/>".format(
        cgi.escape(url, quote=True)
    )
    html += "<b>Parameter: </b>{}<br/>".format(
        cgi.escape(notify_jobs.parameter or "", quote=True)
    )
    html += "<b>Payload: </b>{}<br/>".format(
        cgi.escape(notify_jobs.payload, quote=True)
    )
    html += "<b>Notes: </b>{}<br/>".format(
        cgi.escape(notify_jobs.notes, quote=True)
    )

    html += "https://{}/admin/capture/{}".format(
        app.config.get('HOSTNAME', 'localhost'),
        notify_jobs.id
    )

    # If there are people to email, email them that a capture was recieved
    if email_list:
        if app.config["EMAILS_USE_SES"]:
            import boto.ses
            try:
                ses_region = app.config.get('SES_REGION', 'us-east-1')
                ses = boto.ses.connect_to_region(ses_region)
            except Exception, e:
                import traceback
                app.logger.debug(Exception)
                app.logger.debug(e)
                app.logger.warn(traceback.format_exc())
                return

            for email in email_list:
                try:
                    ses.send_email(
                        app.config['MAIL_SENDER'],
                        subject,
                        html,
                        email,
                        format="html"
                    )
                    app.logger.debug("Emailed {} - {} ".format(email, subject))
                except Exception, e:
                    m = "Failed to send failure message to {} from {} with subject: {}\n{} {}".format(
                        email,
                        app.config['MAIL_SENDER'],
                        subject,
                        Exception,
                        e
                    )
                    app.logger.debug(m)
        else:
            msg = Message(
                subject,
                sender=app.config['MAIL_SENDER'],
                recipients=email_list
            )
            msg.html = html
            try:
                flask_mail.send(msg)
            except Exception as err:
                app.logger.debug(Exception)
                app.logger.debug(err)


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

            if app.config.get('ALLOWED_DOMAINS'):
                domain = urlparse(url).netloc.split(':')[0]
                if domain not in app.config.get('ALLOWED_DOMAINS'):
                    app.logger.info("Ignoring Capture from unapproved domain: [{}]".format(domain))
                    return response

            referrer = urllib.unquote(unicode(request.form.get('referrer', '')))
            cookies = urllib.unquote(unicode(request.form.get('cookies', '')))
            user_agent = urllib.unquote(unicode(request.form.get('user_agent', '')))
            # TODO rename assessment to payload
            assessment = Payload.query.filter_by(id=int(request.form.get('xss_uid', 0))).first()
            xss_uid = assessment # what the heck
            # Payload.query.filter_by(id=int(request.form['xss_uid'])).first()
            screenshot = unicode(request.form.get('screenshot', ''))
            dom = urllib.unquote(unicode(request.form.get('dom', '')))[:65535]

            # If it's a rogue capture, log it anyway.
            if assessment is None:
                client_info = Capture("Not found", url, referrer, cookies, user_agent, 0, screenshot, dom)
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
