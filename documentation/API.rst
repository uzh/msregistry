==============================
MS Registry REST API Resources
==============================

Document Version
----------------

:Date:
    2016-05-02
:Version:
    v0.3.4
:Authors:
    Filippo Panessa <filippo.panessa@gmail.com>
:Copyright:
    Copyright (c) 2016 S3IT, Zentrale Informatik, University of Zurich

Welcome to the MS Registry REST API. Below, you’ll find a full listing of all 
the available  endpoints. As we add more endpoints, they will be automatically 
documented here.

The endpoint’s documentation section includes what query parameters the endpoint
will accept, what the JSON object’s parameters will be in the response, and an 
example query/response.

This documentation is for most recent version of the MS Registry REST API, 
version **v0.4.1**.

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
| **status**    | **code**             | **message**                           |
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
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
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
      "status": 200,
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
| **status**    | **code**             | **message**                           |
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
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | Couldn't found a User with UniqueID={}|
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
      "member_since": "2016-03-04T17:03:37",
      "last_seen": "2016-03-04T17:05:12"
    }

GET /user/consent/info
----------------------

Get detailed informations about user acceptance of Informed Consent.

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/consent/info
      Requires authentication?    Yes
      Requires Role?              Patient, Relative

Response Parameters
```````````````````

Relative Role

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **birthdate**                   | `(string)`      | Birthdate in this form %DD.%MM.%YYYY |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **sex**                         | `(string)`      | Sex. Possibly values are 'male' and  |
|                                 |                 | 'female'                             |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **signature**                   | `(string)`      | Signature by Initials, max 3 digits  |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

Patient Role

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **birthdate**                   | `(string)`      | Birthdate in this form %DD.%MM.%YYYY |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **sex**                         | `(string)`      | Sex. Possibly values are 'male' and  |
|                                 |                 | 'female'                             |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **signature**                   | `(string)`      | Signature by Initials, max 3 digits  |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **physician_contact_permitted** | `(bool)`        | Physician contact permitted          |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **data_exchange_cohort**        | `(bool)`        | Data exchange cohort                 |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **medical_record_abstraction**  | `(bool)`        | Medical record abstraction           |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | Couldn't found a User with UniqueID={}|
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/consent/info'

Response
::::::::

.. code:: json

    {
        "birthdate": "18.09.1974",
        "sex": "M",
        "signature": "FP",
        "data_exchange_cohort": true,
        "date_signed": "2016-03-30T14:33:48.011000",
        "medical_record_abstraction": true,
        "data_exchange_cohort": true,
        "physician_contact_permitted": true
    }

GET /user/consent
-----------------

Get brief information about user acceptance of Informed Consent.

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/consent
      Requires authentication?    Yes
      Requires Role?              Patient, Relative

Response Parameters
```````````````````

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **accepted**                    | `(bool)`        | Return True if Consent Information   |
|                                 |                 | was accepted, False otherwise        |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 400           |token_expired         | Token is expired                      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_audience      | Incorrect audience                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 400           |invalid_signature     | Token signature is invalid            |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | Couldn't found a User with UniqueID={}|
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
        "accepted": true
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

Relative Role

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **birthdate**                   | `(string)`      | Birthdate in this form %DD.%MM.%YYYY |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **sex**                         | `(string)`      | Sex. Possibly values are 'male' and  |
|                                 |                 | 'female'                             |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **signature**                   | `(string)`      | Signature by Initials, max 3 digits  |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

Patient Role

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **birthdate**                   | `(string)`      | Birthdate in this form %DD.%MM.%YYYY |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **sex**                         | `(string)`      | Sex. Possibly values are 'male' and  |
|                                 |                 | 'female'                             |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **signature**                   | `(string)`      | Signature by Initials, max 3 digits  |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **physician_contact_permitted** | `(bool)`        | Physician contact permitted          |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **data_exchange_cohort**        | `(bool)`        | Data exchange cohort                 |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **medical_record_abstraction**  | `(bool)`        | Medical record abstraction           |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

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
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 405           |method_not_allowed    |                                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     -X POST -d '{"physician_contact_permitted": true, \
                  "data_exchange_cohort": true, \
                  "medical_record_abstraction": true, \
                  "sex": "male", \
                  "signature": "FP", \
                  "birthdate": "18.09.1974"}' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/consent'

Response
::::::::

.. code:: json

    {
      "success": true
    }

GET /user/diary
---------------

Get All Diary entries compiled by User.

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/diary
      Requires authentication?    YES
      Requires Role?              Patient, Relative

Request Parameters
``````````````````

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **from**                        | `(iso 8601`     | If used, query returns Diary entries |
|                                 | `datetime)`     | starting from this datetime. It      |
|                                 |                 | could be used in combination with    |
|                                 |                 | *until* parameter                    |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **until**                       | `(iso 8601`     | If used, query returns Diary entries |
|                                 | `datetime)`     | starting from this datetime. It      |
|                                 |                 | could be used in combination with    |
|                                 |                 | *from* parameter                     |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **diaries**         | `(array)`       | Return list of all Diaries compiled  |
|                     |                 | by User as JSON array                |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **id**              | `(string)`      | Return Diary ID                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **diary**           | `(json object)` | Return User's Diary. Returned value  |
|                     |                 | is a JSON object                     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **timestamp**       | `(iso 8601`     | Datetime the diary was inserted or   |
|                     | `datetime)`     | updated                              |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/diary?from=2016-04-01T00:00:00.000000&until=2016-04-09T00:00:00.000000'

Response
::::::::

.. code:: json

    {
        "diaries": [
            {
                "diary": {
                    "value": "any"
                },
                "id": "5707ba42ec71bc038226c84b",
                "timestamp": "2016-04-08T11:36:37.177000"
            }
        ]
    }

GET /user/diary/<id>
--------------------

Get User's Diary by Diary ID.

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/diary/<id>
      Requires authentication?    YES
      Requires Role?              Patient, Relative

Request Parameters
``````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **id**              | `(string)`      | Diary ID                             |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **id**              | `(string)`      | Return Diary ID                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **diary**           | `(json object)` | Return user's Diary. Returned value  |
|                     |                 | is a JSON object                     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **timestamp**       | `(iso 8601`     | Datetime the diary was inserted or   |
|                     | `datetime)`     | updated                              |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | Couldn't found a Diary with id={}     |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/diary/56f2c662ec71bc2c6b001040'

Response
::::::::

.. code:: json

    {
        "id": "5707ba42ec71bc038226c84b",
        "diary": {
            "value": "any"
        },
        "timestamp": "2016-04-08T11:36:37.177000"
    }

POST /user/diary
----------------

Insert new User's Diary entry.

Resource Information
````````````````````

   ::

      Method                      POST
      URL                         /api/v1.0/user/diary
      Requires authentication?    Yes
      Requires Role?              Patient, Relative
      Requires IC Accepted?       Yes

Request Parameters
``````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **diary**           | `(json object)` | Any JSON object                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **success**         | `(bool)`        | Return True if diary is accepted     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Consent Information not accepted      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 405           |method_not_allowed    |                                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     -X POST -d '{"diary": {"any": "value"}}' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/diary'

Response
::::::::

.. code:: json

    {
      "success": true
    }

POST /user/diary/<id>
---------------------

Update User's Diary by Diary ID.

Resource Information
````````````````````

   ::

      Method                      POST
      URL                         /api/v1.0/user/diary/<id>
      Requires authentication?    YES
      Requires Role?              Patient, Relative

Request Parameters
``````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **id**              | `(string)`      | Diary ID                             |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **diary**           | `(json object)` | Any JSON object                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **success**         | `(bool)`        | Return True if diary is accepted     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | Couldn't found a Diary with id={}     |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     -X POST -d '{"diary": {"any": "value"}}' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/diary/56f2c662ec71bc2c6b001040'

Response
::::::::

.. code:: json

    {
      "success": true
    }

GET /user/survey
----------------

Get All Survey entries compiled by User.

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/survey
      Requires authentication?    YES
      Requires Role?              Patient, Relative

Request Parameters
``````````````````

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **from**                        | `(iso 8601`     | If used, query returns Survey entries|
|                                 | `datetime)`     | starting from this datetime. It      |
|                                 |                 | could be used in combination with    |
|                                 |                 | *until*, *tags* and *ongoing*        |
|                                 |                 | parameters                           |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **until**                       | `(iso 8601`     | If used, query returns Survey entries|
|                                 | `datetime)`     | starting from this datetime. It      |
|                                 |                 | could be used in combination with    |
|                                 |                 | *from*, *tags* and *ongoing*         |
|                                 |                 | parameters                           |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **tags**                        | `(array)`       | If used, query returns all entries   |
|                                 |                 | with declared TAGs. It could be used |
|                                 |                 | in combination with *from*, *until*  |
|                                 |                 | and *ongoing* parameters             |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+
| **ongoing**                     | `(bool)`        | If used, query returns all entries   |
|                                 |                 | with ongoing value requested. It     |
|                                 |                 | could be used in combination with    |
|                                 |                 | *from*, *until* and *tags*           |
|                                 |                 | parameters                           |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **surveys**         | `(array)`       | Return list of all Surveys compiled  |
|                     |                 | by User as JSON array                |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **id**              | `(string)`      | Return Survey ID                     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **survey**          | `(json object)` | Return User's Survey. Returned value |
|                     |                 | is a JSON object                     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **timestamp**       | `(iso 8601`     | Datetime the survey was inserted     |
|                     | `datetime)`     |                                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **tags**            | `(array)`       | Return list of all TAGs assigned to  |
|                     |                 | a Survey entry                       |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **ongoing**         | `(bool)`        | Ongoing value is a boolean flag that |
|                     |                 | refer to completed Surveys           |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/survey?from=2016-03-01T00:00:00.000000&until=2016-03-14T00:00:00.000000'

Response
::::::::

.. code:: json

    {
        "surveys": [
            {
                "id": "56f2c662ec71bc2c6b001040",
                "survey": {
                    "value": "any"
                },
                "tags": ["layer2", "other_tag"],
                "ongoing": true,
                "timestamp": "2016-03-03T16:37:54.765000"
            },
            {
                "id": "56f2c7cdec71bc2c6b001041",
                "survey": {
                    "value": "any"
                },
                "tags": ["layer3"],
                "ongoing": false,
                "timestamp": "2016-03-12T17:01:57.800000"
            }
        ]
    }

GET /user/survey/<id>
---------------------

Get User's Survey by Survey ID.

Resource Information
````````````````````

   ::

      Method                      GET
      URL                         /api/v1.0/user/survey/<id>
      Requires authentication?    YES
      Requires Role?              Patient, Relative

Request Parameters
``````````````````

+---------------------------------+-----------------+--------------------------------------+
| **Parameter**                   | **Type**        | **Description**                      |
+=================================+=================+======================================+
| **id**                          | `(string)`      | Survey ID                            |
|                                 |                 |                                      |
+---------------------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **id**              | `(string)`      | Return Survey ID                     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **survey**          | `(json object)` | Return user's Survey. Returned value |
|                     |                 | is a JSON object                     |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **timestamp**       | `(iso 8601`     | Datetime the survey was inserted or  |
|                     | `datetime)`     | updated                              |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **tags**            | `(array)`       | Return list of all TAGs assigned to  |
|                     |                 | a Survey entry                       |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **ongoing**         | `(bool)`        | Ongoing value is a boolean flag that |
|                     |                 | refer to completed Surveys           |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | Couldn't found a Survey with id={}    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/survey/56f2c662ec71bc2c6b001040'

Response
::::::::

.. code:: json

    {
        "id": "56f2c662ec71bc2c6b001040",
        "survey": {
            "value": "any"
        },
        "tags": ["layer2", "other_tag"],
        "ongoing": false,
        "timestamp": "2016-03-23T16:37:54.765000"
    }

POST /user/survey
-----------------

Insert a new User's Survey.

Resource Information
````````````````````

   ::

      Method                      POST
      URL                         /api/v1.0/user/survey
      Requires authentication?    Yes
      Requires Role?              Patient, Relative
      Requires IC Accepted?       Yes

Request Parameters
``````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **survey**          | `(json object)` | Any JSON object                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **tags**            | `(array)`       | List of all TAGs assigned to this    |
|                     |                 | Survey entry. It cannot be null      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **ongoing**         | `(bool)`        | Ongoing value is a boolean flag that |
|                     |                 | refer to completed Surveys. It       |
|                     |                 | cannot be null                       |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **success**         | `(bool)`        | Return True if Survey is accepted    |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 401           |unauthorized          | Consent Information not accepted      |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 405           |method_not_allowed    |                                       |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     -X POST -d '{"survey": {"value": "any"}, "tags": ["layer2"], "ongoing": true}' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/survey'

Response
::::::::

.. code:: json

    {
      "success": true
    }

POST /user/survey/<id>
----------------------

Update User's Survey by Survey ID.

Resource Information
````````````````````

   ::

      Method                      POST
      URL                         /api/v1.0/user/survey/<id>
      Requires authentication?    YES
      Requires Role?              Patient, Relative

Request Parameters
``````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **id**              | `(string)`      | Survey ID                            |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **survey**          | `(json object)` | Any JSON object                      |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **tags**            | `(array)`       | List of all TAGs assigned to this    |
|                     |                 | Survey entry. If null, TAGs are not  |
|                     |                 | updated                              |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+
| **ongoing**         | `(bool)`        | Ongoing value is a boolean flag that |
|                     |                 | refer to completed Surveys. It       |
|                     |                 | cannot be null                       |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Response Parameters
```````````````````

+---------------------+-----------------+--------------------------------------+
| **Parameter**       | **Type**        | **Description**                      |
+=====================+=================+======================================+
| **success**         | `(bool)`        | Return True if Survey is accepted    |
|                     |                 |                                      |
+---------------------+-----------------+--------------------------------------+

Resource Errors
```````````````

These are the possible errors returned by this endpoint.

+---------------+----------------------+---------------------------------------+
| **status**    | **code**             | **message**                           |
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
| 401           |unauthorized          | Insufficient Roles                    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+
| 404           |not_found             | Couldn't found a Survey with id={}    |
|               |                      |                                       |
+---------------+----------------------+---------------------------------------+

Example
```````

.. code:: bash

    curl \
     -H 'authorization: Bearer YOUR_API_TOKEN' \
     -X POST -d '{"survey": {"value": "any"}, "tags": ["layer2", "othertag"], "ongoing": true}' \
     'https://ws.msregistry.s3it.uzh.ch/api/v1.0/user/survey/56f2c662ec71bc2c6b001040'

Response
::::::::

.. code:: json

    {
      "success": true
    }
