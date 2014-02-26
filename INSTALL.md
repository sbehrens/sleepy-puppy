#Install Guide#
##Setup##

Grab the repo

    git clone https://github.com/sbehrens/sleepy-puppy.git
    
Install the required dependencies

    python setup.py install
Create the database

    python manage.py create_db
Create a user to access the application

    python manage.py create_login

Install gunicorn

    pip install gunicorn

Install nginx

on ubuntu: 

    apt-get install nginx
    
on osx: 

    brew install nginx


You will want to setup nginx with signed certificates.  We use the CDN notation when generating blind xss payloads (// vs http://) to save space.  CDN notation resolves to the current scheme, so if you are injecting into a page hosted over ssl, the callbacks will have to be on a web server that supports ssl.   

The following configuration can be copied into the server portion of the nginx.conf file.  Replace the CAPS portion with your information:

```nginx
    server {
        listen 80;
        server_name YOUR_SERVER_NAME.com;
        root /PATH_TO_SLEEPY_PUPPY_ROOT;
    
        access_log /YOUR_LOG_FOLDER/access.log;
        error_log /YOUR_LOG_FOLDER/error.log;
    
        location / {
            proxy_set_header X-Forward-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_pass http://127.0.0.1:8000;
            proxy_connect_timeout 30;
            proxy_read_timeout 30;
        }
    }
    
    server {
        listen 443;
    
        ssl on;
        ssl_certificate YOUR_SSL_CERT_HERE;
        ssl_certificate_key YOUR_SSL_KEY_HERE;
    
        server_name crushit.today;
        access_log /YOUR_LOG_FOLDER/access.log;
        error_log /YOUR_LOG_FOLDER/error.log;
    
        location / {
            # checks for static files; if not found, proxy to app
            try_files $uri @proxy_to_app;
        }
    
        location @proxy_to_app {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
    
            proxy_pass http://127.0.0.1:8000;
        }
    
    }
```    

Double check everything is okay by running the following:

    nginx -t
    
You need to start gunicorn

    cd /where_you_put_sleepy_puppy
    gunicorn sleepypuppy:app
    
    
Start nginx
    
    nginx

##Persistance##

If you reboot, nginx won't know how to start gunicorn.  Try [Supervisor](http://www.supervisor.io):

    sudo pip install supervisor

Supervisor is going to look for this supervisord.conf file in a few places by default:

    /usr/local/share/etc/supervisord.conf
    /usr/local/share/supervisord.conf
    ./supervisord.conf
    ./etc/supervisord.conf
    /etc/supervisord.conf

Here is an example configuration file (supervisord.conf):

    [program:sleepypuppy]
    command = gunicorn sleepypuppy:app
    directory = /PATH_TO_SLEEPY-PUPPY
    user = root
    
Restart supervisor:

    supervisorctl reread
    supervisorctl update
    supervisorctl start sleepypuppy
