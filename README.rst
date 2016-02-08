========================================================================
    MSRegistry Backend
========================================================================

.. This file follows reStructuredText markup syntax; see
   http://docutils.sf.net/rst.html for more information


MSRegistry Backend is the WEB Backend for Swiss Multiple Sclerosis Registry.
It's developed in Python using Flask Framework.


Installation instructions
=========================

Before install *MSRegistry* I suggest to prepare a Python virtual environment
using `virtualenv`:

.. code-block:: bash
    virtualenv env
    source env/bin/active

Now we can easily install Python dependencies: 

.. code-block:: bash
    pip install -r requirements/common.txt


Deploy Database and run Web Application
=======================================

Using `manage.py` we can create initial empty database

.. code-block:: bash
    python manage.py db init
    python manage.py db migrate
    python manage.py create``

and run Web application

.. code-block:: bash
    python manage.py runserver``


**********
References
**********

.. target-notes::

.. _`Flask`: http://flask.pocoo.org/
.. _`SQLAlchemy`: http://www.sqlalchemy.org/
.. _`Alembic`: https://alembic.readthedocs.org/
