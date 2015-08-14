import urllib
from flask import request
from flask import render_template, make_response
from flask_mail import Message
from sleepypuppy import app, db, flask_mail, csrf_protect
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.collector.models import GenericCollector
from sleepypuppy.admin.access_log.models import AccessLog
from sleepypuppy.admin.assessment.models import Assessment
from sleepypuppy.admin.user.models import User
from flask import Response
from urlparse import urlparse


@app.route('/x', methods=['GET'])
def x_collector(payload_id=1):
    """
    Determine the payload assocaited with the request.
    If accesslog is enabled for the payload, record the event
    and email users subscribed to the payload's assessment.
    """

    # consider only looking up payload one time for performance
    the_payload = Payload.query.filter_by(id=int(payload_id)).first()

    for assessment_name in the_payload.assessments:
        print assessment_name
        the_assessment = Assessment.query.filter_by(
            name=str(assessment_name)).first()
        if the_assessment.access_log_enabled:
            try:
                referrer = request.headers.get("Referrer", None)
                user_agent = request.headers.get("User-Agent", None)
                ip_address = request.remote_addr
                client_info = AccessLog(
                    payload_id, referrer, user_agent, ip_address)
                db.session.add(client_info)
                db.session.commit()
            except Exception as err:
                app.logger.warn(err)
            try:
                email_subscription(payload_id, None, client_info, 'access_log')
            except Exception as err:
                app.logger.warn(err)
        break
    # Log for recording access log records
    if request.args.get('u', 1):
        return collector(request.args.get('u', 1))


@app.route('/loader.js', methods=['GET'])
def collector(payload_id=1):
    """
    Render Javascript payload with unique identifier and hosts for callback.
    Enforce snooze and run_once directives.
    """
    payload_id = request.args.get('u', 1)
    try:
        the_payload = Payload.query.filter_by(id=int(payload_id)).first()
        if the_payload.snooze:
            return ''
        if the_payload.run_once and Capture.query.filter_by(payload_id=int(payload_id)).first():
            return ''
    except Exception as err:
        app.logger.warn(err)

    # Render the template and include payload_id, hostname, callback_protocol.
    # If you need to expose additiional server side
    # information for your JavaScripts, do it here.
    headers = {'Content-Type': 'text/javascript'}
    return make_response(render_template(
        'loader.js',
        payload_id=payload_id,
        hostname=app.config['CALLBACK_HOSTNAME'],
        callback_protocol=app.config.get('CALLBACK_PROTOCOL', 'https')),
        200,
        headers
    )


def email_subscription(payload_id, url, client_info, model):
    """
    Email notifications for captures, generic collections, and access log
    """
    email_list = []
    notify_jobs = Payload.query.filter_by(id=payload_id).first()
    user_notify = User.query.all()
    for user in user_notify:
        user_subscriptions = []
        for assessment in user.assessments:
            user_subscriptions.append(assessment.id)
        if len(set(notify_jobs.show_assessment_ids()).intersection(user_subscriptions)) > 0:
            email_list.append(user.email)

    import cgi
    if model == "capture":
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

        html += "<b>Capture: </b>{}://{}/admin/capture/?flt1_0={}".format(
            app.config.get('CALLBACK_PROTOCOL', 'https'),
            app.config.get('HOSTNAME', 'localhost'),
            client_info.id)

    elif model == "access_log":
        subject = "[Sleepy Puppy] - Access Log Request Recieved For Assessment(s): {}".format(
            cgi.escape(notify_jobs.show_assessment_names(), quote=True)
        )
        html = "<b>Associated Assessments: </b>{}<br/>".format(
            cgi.escape(notify_jobs.show_assessment_names(), quote=True)
        )
        html += "<b>Referer: </b>{}<br/>".format(
            cgi.escape(client_info.referrer or "", quote=True)
        )
        html += "<b>User Agent: </b>{}<br/>".format(
            cgi.escape(client_info.user_agent or "", quote=True)
        )
        html += "<b>IP Address: </b>{}<br/>".format(
            cgi.escape(client_info.ip_address, quote=True)
        )

        html += "<b>AccessLog: </b>{}://{}/admin/accesslog/?flt1_0={}".format(
            app.config.get('CALLBACK_PROTOCOL', 'https'),
            app.config.get('HOSTNAME', 'localhost'),
            client_info.id)

    elif model == "generic_collector":
        subject = "[Sleepy Puppy] - Generic Collector Recieved From: {}".format(
            cgi.escape(client_info.url, quote=True)
        )
        html = "<b>Associated Assessments: </b>{}<br/>".format(
            cgi.escape(notify_jobs.show_assessment_names(), quote=True)
        )
        html += "<b>Javascript Name: </b>{}<br/>".format(
            cgi.escape(client_info.javascript_name or "", quote=True)
        )
        html += "<b>Url: </b>{}<br/>".format(
            cgi.escape(client_info.url or "", quote=True)
        )
        html += "<b>Referer: </b>{}<br/>".format(
            cgi.escape(client_info.referrer or "", quote=True)
        )

        html += "<b>Generic Collector: </b>{}://{}/admin/genericcollector/?flt1_0={}".format(
            app.config.get('CALLBACK_PROTOCOL', 'https'),
            app.config.get('HOSTNAME', 'localhost'),
            client_info.id)

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


@csrf_protect.exempt
@app.route('/generic_callback', methods=['POST', 'GET'])
def get_generic_callback():
    """
    Method to handle generic callbacks from arbitrary javascripts.

    Expects
    Method:          POST
    Data:            payload_id, javascript_name, data
    Optional Data:   referrer, url
    """
    response = Response()

    app.logger.info("Inside /generic_callback")

    if request.method == 'POST':
        try:
            app.logger.info("request.form.get('payload_id', 0): {}".format(
                request.form.get('payload_id', 0)))

            javascript_name = urllib.unquote(
                unicode(request.form.get('javascript_name', '')))

            # If they don't set a url or referrer, ignore it
            url = urllib.unquote(unicode(request.form.get('uri', '')))
            referrer = urllib.unquote(
                unicode(request.form.get('referrer', '')))

            try:
                if app.config.get('ALLOWED_DOMAINS'):
                    domain = urlparse(url).netloc.split(':')[0]
                    if domain not in app.config.get('ALLOWED_DOMAINS'):
                        app.logger.info(
                            "Ignoring Capture from unapproved domain: [{}]".format(domain))
                        return response
            except Exception as e:
                app.logger.warn("Exception in /generic_callback when parsing url {}\n\n{}".format(Exception, str(e)))  # noqa

            data = urllib.unquote(unicode(request.form.get('data', '')))

            payload = Payload.query.filter_by(
                id=int(request.form.get('payload_id', 0))).first()

            # If it's a rogue capture, log it anyway.
            if payload is None:
                client_info = GenericCollector(
                    0, javascript_name, url, referrer, data)
            else:
                # Create the capture with associated assessment/payload
                client_info = GenericCollector(
                    payload.id, javascript_name, url, referrer, data)

            db.session.add(client_info)
            db.session.commit()
            # Email users subscribed to the Payload's Assessment
            email_subscription(
                payload.id, url, client_info, 'generic_collector')
        except Exception as e:
            app.logger.warn(
                "Exception in /generic_callback {}\n\n{}".format(Exception, str(e)))
            import traceback
            traceback.print_exc()

    return response


# Disable CSRF protection on callback posts
@csrf_protect.exempt
@app.route('/callbacks', methods=['POST', 'GET'])
def get_callbacks():
    """
    Method to handle Capture creation.

    The Default Javascript provides all the expected parameters
    for this endpoint.

    If you need to modify the default captures, provide the following:

    Method:   POST
    Data:     assessment(payload.id will work here), url, referrer, cookies, user_agent, payload_id,
              screenshot, dom
    """
    response = Response()

    app.logger.info("Inside /callbacks")

    if request.method == 'POST':
        try:
            app.logger.info("request.form.get('payload_id', 0): {}".format(
                request.form.get('payload_id', 0)))

            url = urllib.unquote(unicode(request.form.get('uri', '')))

            if app.config.get('ALLOWED_DOMAINS'):
                domain = urlparse(url).netloc.split(':')[0]
                if domain not in app.config.get('ALLOWED_DOMAINS'):
                    app.logger.info(
                        "Ignoring Capture from unapproved domain: [{}]".format(domain))
                    return response

            referrer = urllib.unquote(
                unicode(request.form.get('referrer', '')))
            cookies = urllib.unquote(unicode(request.form.get('cookies', '')))
            user_agent = urllib.unquote(
                unicode(request.form.get('user_agent', '')))
            # TODO rename assessment to payload
            payload = Payload.query.filter_by(
                id=int(request.form.get('payload_id', 0))).first()
            screenshot = unicode(request.form.get('screenshot', ''))
            dom = urllib.unquote(unicode(request.form.get('dom', '')))[:65535]
            # If it's a rogue capture, log it anyway.
            if payload is None:
                client_info = Capture("Not found",
                                      url,
                                      referrer,
                                      cookies,
                                      user_agent,
                                      0,
                                      screenshot,
                                      dom)
            else:
                # Create the capture with associated assessment/payload
                client_info = Capture(payload.id,
                                      url,
                                      referrer,
                                      cookies,
                                      user_agent,
                                      payload.id,
                                      screenshot,
                                      dom)

            db.session.add(client_info)
            db.session.commit()
            # Email users subscribed to the Payload's Assessment
            email_subscription(payload_id.id, url, client_info, 'capture')
        except Exception as e:
            app.logger.warn(
                "Exception in /callbacks {}\n\n{}".format(Exception, str(e)))
            import traceback
            traceback.print_exc()

    return response
