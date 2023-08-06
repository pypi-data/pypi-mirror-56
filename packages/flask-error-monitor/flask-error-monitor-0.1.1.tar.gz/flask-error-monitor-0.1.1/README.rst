==============================
Flask Error Monitor
==============================

Full featured error monitor app for Flask

.. image:: https://travis-ci.org/sonus21/flask-error-monitor.svg?branch=master
    :target: https://travis-ci.org/sonus21/flask-error-monitor

.. image:: https://coveralls.io/repos/github/sonus21/flask-error-monitor/badge.svg
    :target: https://coveralls.io/github/sonus21/flask-error-monitor

Introduction
------------

Flask-Error-Monitor is a batteries-included, simple-to-use `Flask <http://flask.pocoo.org/>`_ extension that lets you
add error recording interfaces to Flask applications. It's implemented in such a way that the developer has total control of the resulting application.

Out-of-the-box, Flask-Error-Monitor plays nicely with various ORM's, including

- `SQLAlchemy <http://www.sqlalchemy.org/>`_,

- `MongoEngine <http://mongoengine.org/>`_,


It also boasts a simple Model management interface.

The biggest feature of Flask-Error-Monitor is flexibility. To start off with you can create a very simple application in no time,
with exception monitor enabled, but then you can go further and customize different aspects.

Flask-Error-Monitor is an active project, well-tested and production ready.

Installation
------------
To install Flask-Error-Monitor, simply::

    pip install flask-error-monitor.git


Features
--------
- Sensitive data( like *password*, *secret* ) Masking
- Record all the frames ( frame data are stored in JSON format so that it can be analyzed later)
- Unique URL generation
- Number of times the exception occurred and first/last time of exception
- Sending emails with exception details
- Record different types of exception like 500 or 404 etc
- Raise or update ticket in Jira/Bugzilla etc by ticketing interface.

Usage
-----

* App configuration

.. code::

    ...
    APP_ERROR_SEND_EMAIL = True
    APP_ERROR_RECIPIENT_EMAIL = ('example@example.com',)
    APP_ERROR_SUBJECT_PREFIX = "Server Error"
    APP_ERROR_EMAIL_SENDER = 'user@example.com'



app.py

.. code::

    from flask import Flask
    from flask_mail import Mail
    import settings
    from flask_error_monitor import AppErrorMonitor
    from flask_sqlalchemy import SQLAlchemy
    ...
    app = Flask(__name__)
    app.config.from_object(settings)
    db = SQLAlchemy(app)
    class MyMailer(Mail, NotificationMixin):
        def notify(self, message, exception):
            self.send(message)
    mail = MyMailer(app=app)
    error_monitor = AppErrorMonitor(app=app, db=db, notifier=mail)

    ....

    ....
    # Record exception when 404 error code is raised
    @app.errorhandler(403)
    def error_403(e):
        error_monitor.record_exception()
        # any custom logic

    # Record error using decorator
    @app.errorhandler(500)
    @error_monitor.track_exception
    def error_500(e):
        # some custom logic
    ....



Documentations
--------------
This has got extensive document browse at https://flask-error-monitor.readthedocs.io/en/latest/

All docs are in `docs/source`

And if you want to preview any *.rst* snippets that you may want to contribute, go to `http://rst.ninjs.org/ <http://rst.ninjs.org/>`_.


Examples
--------
Several usage examples are included in the */tests* folder. Please feel free to add your own examples, or improve
on some of the existing ones, and then submit them via GitHub as a *pull-request*.

You can see some of these examples in action at https://github.com/sonus21/flask-error-monitor/tree/master/examples.
To run the examples on your local environment, one at a time, do something like::

    cd flask-error-monitor
    python examples/simple/app.py


Tests
-----
Test are run with *nose*. If you are not familiar with this package you can get some more info from `their website <https://nose.readthedocs.io/>`_.

To run the tests, from the project directory, simply::

    pip install -r requirements-dev.txt
    nosetests

You should see output similar to::

    .............................................
    ----------------------------------------------------------------------
    Ran 29 tests in 1.144s

    OK


Contribution
-------------
You're most welcome to raise pull request or fixes.
