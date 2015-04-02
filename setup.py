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
    'Flask-Admin==1.0.7',
    'Flask-Bcrypt==0.5.2',
    'Flask-Login==0.2.9',
    'Flask-Mail==0.9.0',
    'Flask-RESTful==0.2.11',
    'Flask-SQLAlchemy==1.0',
    'Flask-Script==0.6.3',
    'Flask-WTF==0.9.4',
    'Pillow==2.7.0',
    'SQLAlchemy==0.9.3',
    'bcrypt==1.1.1',
    'psycopg2'
       ]
)
