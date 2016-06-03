========================================================================
    Locust load testing
========================================================================

.. This file follows reStructuredText markup syntax; see
   http://docutils.sf.net/rst.html for more information

Locust performs a load testing.

Install
=======

Before install **Locust load testing** I suggest to prepare a Python virtual
environment using `virtualenv`:

   ::

      $ virtualenv env
      $ source env/bin/active

Now you can easily install Python dependencies:

   ::

      $ pip install -r requirements.txt


Config
======

Locust configuration file is ``locust.yml``.

Lanch test
==========

   ::

      $ locust -f locustfile.py --host=http//you.backend.api.url

.. References

.. _`Locust`: http://locust.io/
