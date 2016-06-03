========================================================================
    MSRegistry Backend
========================================================================

.. This file follows reStructuredText markup syntax; see
   http://docutils.sf.net/rst.html for more information


MSRegistry Backend is the WEB Backend for **Swiss Multiple Sclerosis Registry**.
It's developed in Python using Flask Framework.


Install
=======

Before install **MSRegistry** I suggest to prepare a Python virtual environment
using `virtualenv`:

   ::

      $ virtualenv env
      $ source env/bin/active

Now you can easily install Python dependencies:

   ::

      $ cd msregistry
      $ pip install -r requirements/common.txt


Deploy Database and run Web Application
=======================================

Use ``flask`` to run Web application

   ::

      $ export FLASK_APP=commands.py
      $ flask run

Config
======

MSRegistry Backend configuration file is ``config.yml``.


.. References

.. _`Flask`: http://flask.pocoo.org/
.. _`MongoAlchemy`: http://www.mongoalchemy.org/
