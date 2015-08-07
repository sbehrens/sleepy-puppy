import os
from setuptools import setup

setup(
    name='sleepypuppy',
    version='0.2',#'$$VERSION$$',
    long_description=__doc__,
    packages=['sleepypuppy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.10.1',
        'WTForms==2.0.2',
        'Flask-Admin==1.2.0',
        'Flask-Bcrypt==0.6.2',
        # First0.2.11
        'Flask-Login==0.2.11',
        'Flask-Mail==0.9.1',
        #updated
        'Flask-RESTful==0.3.4',
        'Flask-SQLAlchemy==2.0',
        'Flask-Script==2.0.5',
        'Flask-SSLify==0.1.5',
        'Flask-WTF==0.11',
        'Pillow==2.8.2',
        'SQLAlchemy==1.0.5',
        'bcrypt==2.0.0',
        'gunicorn==19.3.0',
        'psycopg2==2.6.1',
        'boto==2.38.0',
        'BeautifulSoup',
        'flask-migrate'
    ]
)
