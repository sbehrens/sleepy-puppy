import os
from setuptools import setup

setup(
    name='sleepypuppy',
    version='0.1',#'$$VERSION$$',
    long_description=__doc__,
    packages=['sleepypuppy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
            'Flask==0.10.1',
            'Flask-SQLAlchemy==1.0',
            'Flask-Script==0.6.3',
            'SQLAlchemy',
            'bcrypt',
            'Flask-Admin',
            'Flask-WTF',
            'flask-bcrypt',
            'Flask-RESTful',
            'flask-login',
            'Pillow',
            'flask-mail',
        ]
)
