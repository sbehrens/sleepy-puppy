Sleepy Puppy
============

![Sleepy Puppy](http://i.snag.gy/VQfEE.jpg)

##What is Sleepy Puppy?##

Sleepy Puppy is a blind cross-site scripting (xss) collector which was created to simplify blind xss testing.  

##Why Should I use Sleepy Puppy?##
Often when testing for client side injections (HTML/JS/etc.) security engineers are looking for where the injection occurs within the application they are testing *only*.  While this provides ample coverage for the application in scope, there is a possibility that the code engineers are injecting may be reflected back in a completely separate application.  

Sleepy Puppy helps facilitate inter-application xss testing by providing JavaScript payloads that callback to the Sleepy Puppy application. 

##How Does Sleepy Puppy Do It?##

Sleepy Puppy provides a JavaScript payload that security engineers can use for Blind xss testing.  The callback functions provided by the Javascript generate useful capture metadata including the uri, DOM, user-agent, cookies, referer header, and a screenshot where the payload executed.  This allows a tester to generate unique JavaScript payloads and trace what applications they execute in throughout the payload lifecycle.  

Sleepy Puppy also supports email notifications for captures received for specific assessments. 

Sleepy Puppy exposes an API for users who may want to develop plugins for scanners such as Burp or Zap.

[API Documentation](https://github.com/sbehrens/sleepy-puppy/wiki/API)
#Release History#
V0.1 Alpha - 2/26/2014
* Initial release

V0.2 "OWASP Beta Release" - 7/9/2015
* Updated a number of third party dependencies
* Bug fixes for jQuery and Email Notifications
* Amazon S3 storage configuration is now available for screenshots
* Amazon SES email support is now available
* Allowed domains config directive allows users to whitelist which domains to log captures for
* Callback configuration settings for hostname and protocol now supported
* PEP 8 changes (thanks @monkey_security)
* manage.py now supports a new commnad 'create_bootstrap_assessment' which adds a number of example payloads and an example assessment
* Added comprehensive Wiki documentation


#Documentation#
Documentation is maintained in the Github [Wiki](https://github.com/sbehrens/sleepy-puppy/wiki)
