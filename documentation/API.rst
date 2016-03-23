==============================
MS Registry REST API Resources
==============================

Document Version
----------------

Welcome to the MS Registry REST API. Below, you’ll find a full listing of all 
the available  endpoints. As we add more endpoints, they will be automatically 
documented here.

The endpoint’s documentation section includes what query parameters the endpoint
will accept, what the JSON object’s parameters will be in the response, and an 
example query/response.

This documentation is for most recent version of the MS Registry REST API, 
version **v0.3.0**.

GET /auth/test
--------------

Test Bearer Token authentication.

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /auth/test
      Requires authentication?    Yes
      Requires Role?              Every Role can access

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/auth/test'


Response
::::::::

.. code:: json

    {
      "code": "authorization_success", 
      "description": "All good. You only get this message if you're authenticated."
    }

GET /user
---------

Get metadata about the current user.

Resource Information
````````````````````
   ::

      Method                      GET
      URL                         /api/v1.0/user
      Requires authentication?    Yes
      Requires Role?              Every Role can access

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **uniqueID**        | `(string)`      | That's the  unique ID of the user,   |
|                     |                 | received from OAuth server           |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **consent**         | `(bool)`        | Has the Informed Consent been        |
|                     |                 | accepted?                            |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **member\_since**   | `(iso 8601`     | Datetime the user joined             |
|                     | `datetime)`     |                                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **last\_seen**      | `(iso 8601`     | Datetime last seen user. This field  |
|                     | `datetime)`     | is updated on every user interaction |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | User not found                        |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user'

Response
::::::::

.. code:: json

    {
      "uniqueID": "auth0|569cf82bfc02d8a0339beef4",
      "consent": true,
      "member_since": "2016-03-04T17:03:37",
      "last_seen": "2016-03-04T17:05:12"
    }

GET /user/consent
-----------------

Get information about user acceptance of Informed Consent. 

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/consent
      Requires authentication?    Yes
      Requires Role?              Patient, Relative

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **consent**         | `(bool)`        | Has the Informed Consent been        |
|                     |                 | accepted?                            |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/consent'

Response
::::::::

.. code:: json

    {
        "consent": true
    }

POST /user/consent
------------------

Set user acceptance of Informed Consent. 

Resource Information
````````````````````

   ::

      Method                      POST
      URL                         /api/v1.0/user/consent
      Requires authentication?    Yes
      Requires Role?              Patient, Relative

Request Parameters
``````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **consent**         | `(bool)`        | Set True is Informed Consent has     |
|                     |                 | been accepted, False otherwise       |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **success**         | `(bool)`        | Return True if content was accepted  |
|                     |                 | and registered, False otherwise      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -i -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -X POST -d "{'consent': true}" \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/consent'

Response
::::::::

.. code:: json

    {
      "success": true
    }


GET /user/roles
---------------

Get User's Roles. 

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/roles
      Requires authentication?    YES
      Requires Role?              Every Role can access

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **roles**           | `(array)`       | Return user's roles stored on OAuth  |
|                     |                 | Server. Returned values are:         |
|                     |                 | 'doctor', 'guest', 'patient',        |
|                     |                 | 'relative', 'researcher'.            |
|                     |                 | If no roles are stored on OAuth      |
|                     |                 | Server, return empty array.          |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/roles'

Response
::::::::

.. code:: json

    {
      "roles": [
        "doctor", 
        "patient"
      ]
    }

GET /user/lang
--------------

Get User's Language. 

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/lang
      Requires authentication?    YES
      Requires Role?              Every Role can access

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **lang**            | `(string)`      | Return user's language setting       |
|                     |                 | stored on OAuth Server. Returned     |
|                     |                 | values are: 'de', 'fr', 'it'.        |
|                     |                 | If no language setting is stored on  |
|                     |                 | OAuth Server, return default         |
|                     |                 | language 'de'.                       |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/lang'

Response
::::::::

.. code:: json

    {
      "lang": "de"
    }

GET /diary
--------------

Get User's Diary. 

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/diary
      Requires authentication?    YES
      Requires Role?              Patient, Relative

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **diary**           | `(json file)`   | Return user's Diary. Returned value  |
|                     |                 | is a RAW JSON file                   |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **timestamp**       | `(iso 8601`     | Datetime the diary was updated       |
|                     | `datetime)`     |                                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/diary'

Response
::::::::

.. code:: json

    {
        "diary": {
            "value": "any"
        }, 
        "timestamp": "2016-03-23T15:03:41.643000"
    }

POST /diary
------------------

Write User's Diary or Update it. In case of Update, Backend keeps track of
previous Diary versions.

Resource Information
````````````````````

   ::

      Method                      POST
      URL                         /api/v1.0/diary
      Requires authentication?    Yes
      Requires Role?              Patient, Relative
      Requires IC Accepted?       Yes

Request Parameters
``````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **diary**           | `(json file)`   | RAW JSON file                        |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **success**         | `(bool)`        | Return True if diary was accepted,   |
|                     |                 | False if JSON File is not well       |
|                     |                 | formatted                            |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **HTTP Code** | **Error Identifier** | **Error Message**                     |
+===============+======================+=======================================+
| 403           |authorization_required| Authorization header is expected      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must start with  |
|               |                      | Bearer                                |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Token not found                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |invalid_header        | Authorization header must be Bearer + |
|               |                      | token                                 |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 500           |internal_server_error | An error occurred while adding this   |
|               |                      | user                                  |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -i -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     -X POST -d "{'value': 'any'}" \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/diary'

Response
::::::::

.. code:: json

    {
      "success": true
    }
