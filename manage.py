#!/usr/bin/env python
import os
import time
import json
import sys
from random import randint

from flask_script import Command, Option
from flask_script.commands import ShowUrls, Clean
from flask.ext.script import Manager, Server
from sleepypuppy.admin.admin.models import Admin
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
def create_login():
    """
    Seed the database with some inital values
    """
    import getpass

    print 'creating admin user'

    login = raw_input('login: ')
    password = getpass.getpass('password: ')
    confirm_password = getpass.getpass('confirm password: ')

    if Admin.query.filter_by(login=login).count():
        print 'user already exists!'
        sys.exit(1)
    else:
        if password != confirm_password:
            print 'passwords to not match!'
            sys.exit(1)
        else:
            admin_user = Admin(login=login, password=password)
            print 'user: ' + login + ' created!'


    db.session.add(admin_user)
    db.session.commit()
    return

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
