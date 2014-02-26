Sleepy Puppy
============
                                __
         ,                    ," x`--o
        ((                   (  | __,'
         \\~----------------' \_;/
    hjw  (   alert('yawn')      /
         /) ._______________.  )
        (( (               (( (
         ``-'               ``-'


#Overview#
Sleepy Puppy is a blind cross-site scripting (xss) collector which was created to simplify blind xss testing.  Sleepy Puppy contains five types of models: 
* [Assessments](#assessments) - where we setup what we are assessing
* [Payloads](#payloads) - where we log what we are testing
* [Captures](#captures) - where the application collects triggered payloads
* [Users](#users) - where we setup email notifications for captures
* [Admins](#admins) - where we setup accounts for Sleepy Puppy and provision API keys

You simply need to specify a payload record, which contains metadata on where you are testing for blind-xss as well as a placeholder for the Payload.  

The application generates a unique JavaScript payload which scrapes the following information upon execution:

* URI
* DOM
* User-Agent
* Cookies
* Referrer
* Screenshot (Using [HTML2Canvas] (http://html2canvas.hertzen.com/))

The information is presented in an easy to manage tables using Flask-Admin.  

A [User](#users) model allows you to optionally setup email notifications for captures recieved for specific assessments.  Simply specify your email address and what assessments you want to be notified for, and each time a capture is recieved for that assessment you will recieve an email.  

Sleepy Puppy also provides an API for user's who may want to develop plugins for scanners such as Burp or Zap.

[API Documentation](https://github.com/sbehrens/sleepy-puppy/blob/master/api.md)

#Setup#

##Try it Out##

Grab the repo

    git clone https://github.com/sbehrens/sleepy-puppy.git
    
Install the required dependencies

    python setup.py install
Create the database

    python manage.py create_db
Create a user to access the application

    python manage.py create_login
Start the server on localhost:5000

    python manage.py runserver

##Installation##

The [installation guide](https://github.com/sbehrens/sleepy-puppy/blob/master/INSTALL.md) uses the following stack:

[Flask](http://flask.pocoo.org/) + [Gunicorn](http://gunicorn.org/) + [Nginx](http://wiki.nginx.org/Main)
    

#Why Blind Cross-site Scripting?#

Often when we are testing for client side injections (HTML/JS/etc.) we are looking for where the injection occurs within the application we are testing *only*.  While this provides ample coverage for the application in scope, there is a possiblity that the code we are injecting may be reflected back in a completley separate application.  

An examle would be a signup for an eCommerce website.  We can imagine a field such as "First Name" which gets reflected back throughout the eCommerce website.  But what about the helpdesk application when a user has a question?  We can imagine that first name field may get reflected back out in tha helpdesk application.  It's also possible that the help desk user logs into another application to retreive more information on you when you ask a question.  That application may also query the "First Name" parameter.  

Blind cross-site scripting allows you to test a deeper scope and breadth of the 'data' flow within an endpoint.  


#Configuration#

The following configuration file is located in the root of Sleepy Puppy (config-default.py).
```python
    import os
    
    _basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Enable debug mode of Flask
    DEBUG = True
    
    # Application secret key
    SECRET_KEY = "thisIs_soS_ecret_shh!!don'ttell"
    
    # Enable CSRF protection
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "thisistheawes0mestkeytohaveever!!!"
    
    # URI for database 
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/2sleepypuppy.db'
    
    # Location where to store screenshots for captures (png files)
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # Setup debug logging
    LOG_LEVEL = "DEBUG"
    LOG_FILE = "sleepypuppy.log"
    
    # Hostname where you are running Sleepy Puppy
    HOSTNAME = 'crushit.today'
    
    # Email server configuration
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_SENDER = 'sbehrens@netflix.com'
    #MAIL_USE_TLS = False
    #MAIL_USE_SSL = False
    #MAIL_USERNAME = 'you'
    #MAIL_PASSWORD = 'your-password'
```


#Models#
##Admin##
Admin is where you can setup how user access to sleepy puppy.  All users who are a member of the Admin model have the same permissions.  

###Admin View###
![Admin View](http://i.snag.gy/D5LI4.jpg "Admin View")

The Admin view lists the members who have access to sleepy puppy.  In addition, an API key is generated that must be used to access the API.  More information can be found in the [API Documentation.](https://github.com/sbehrens/sleepy-puppy/blob/master/api.md)

###Create an Admin###

There are two ways to create an admin account.  The first is via command line:
    
    python manage.py create_login
                                
The second is via the Admin page (once you are autheticated):

![Create Admin](http://i.snag.gy/bmuGA.jpg "Create Admin")


##Assessments##
Assessments are where you specify the application you are testing.  You will use these assessments for email notfications for users who want to recieve notification when a capture is recieved for a particular assessment.

![Assessment View](http://i.snag.gy/HNzjH.jpg "Assessment View")

##Users##
The User model allows you to specify email notifications for specific assessments.  A user can subscribe to notifications for multiple assessments.

###User View###
![User View](http://i.snag.gy/OfJed.jpg "User View")

There are two users in this example that will recieve notifications when a capture is recieved for a particular assessment.

###Create User###
![Create User](http://i.snag.gy/4Y3HZ.jpg "Create User")

Simply specify your email address and what assessments you would like to recieve notifications for.  


##Payloads##
Payloads are where you specify what and how you are testing the application.  You provide some simple metadata as well as a placeholder where the application will automatically inject the JavaScript payload used to track the capture.  

###Viewing Payloads###
![Payload View](http://i.snag.gy/wm4pM.jpg "Payload View")

The Payload view is a collection of all of the Paylods you have created for testing blind cross-site scripting.  Payloads that have Captures will have a "Yes" in the Captured column.  

###Creating Payloads###
![Payload Create](http://i.snag.gy/henjz.jpg "Payload Create")

When creating payloads, provide the Payload string.  Use the *$1* placeholder for the payload so Sleepy Puppy can automatically build you out a custom JavaScript file.  

The rest of the fields are optional.

Next, copy the Payload from the Payload View and inject it in the application you are testing.  


##Captures##
Captures are where you can view all of the triggered cross-site scripting events.  

###Viewing Captures###
![Capture View](http://i.snag.gy/vVg5u.jpg "Capture View")
After Sleepy Puppy collects a capture, you can view a table containing the captures.  We see here that we have 2 captures with the same ID, letting us know that the Payload was executed two times in the same applications.  We can see this based on the different screenshots and information collected.

You can examine the captured cookies:

![Cookie View](http://i.snag.gy/0UKHZ.jpg "Cookie View")

As well as the DOM, which also hightlights where in the code your payload was executed:

![DOM View](http://i.snag.gy/X4NLK.jpg "DOM View")


##How Collection Works##
After a Payload is generated, the attacker injects the payload into the application.  When the script is loaded in a future time the follwoing events occur:

1.  The JavaScript file is retrieved from the server, passing the *u* parameter which contains a unique identifier used to link the payload with the capture.  The server also replaces associated variables and hostnames within the JavaScript file.  

2.  Script loads Jquery and HTML2Canvas frameworks

3.  Script POSTS to /callbacks and includes: 

    URI,
    Referrer,
    Cookies,
    User Agent,
    DOM,
    Screenshot ID,
    Payload Callback

4.  Script POSTS to /up and includes a screenshot of the capture stored in binary PNG format.

##Email Notifications##
Users who want to recieve notifications can simply edit the User model.  To setup the email server settings, edit the *config-default.py* file.  

An example email notification is below:

![Email Notifications](http://i.snag.gy/Wy95X.jpg "Email Notifications")


##TODO##

Common Payload database (drop down menu)

Encoding options for payload

ZeroCopy clipboard

##Known Issues##
The Flask-Admin framework is vulnerable to [Open Redirect](http://cwe.mitre.org/data/definitions/601.html), but you shoudn't have the Flask Admin pages publically accessible anyway.  I'll try to get a pull request in to Flask-admin to fix that at some point.  
