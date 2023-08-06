# -*- coding: utf-8 -*-
#
#    Flask error monitor's app monitor, that initialize it's internal state
#
#    :copyright: 2018 Sonu Kumar
#    :license: BSD-3-Clause
#


import sys
import traceback
from hashlib import sha256

from warnings import warn

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack
from flask import request

from flask_mail import Message
from .exception_formatter import format_exception
from .utils import Masking, ConfigError
from .mixins import ModelMixin
from .view import Views
from . import defaults
import datetime

from sqlalchemy import Column, String, Text, Integer, DateTime, desc
from sqlalchemy.orm.exc import NoResultFound

page_size = None


class AppErrorMonitor(object):
    def __init__(self, app=None, db=None, model=None, notifier=None, recipients=None,
                 db_table_name="app_error", notification_subject_prefix=None,
                 url_prefix=None, masking=None, ticketing=None,
                 context_builder=defaults.DefaultContextBuilder()):
        """
        An error monitor class, which manage the exception and store them to database
        :param app: a Flask app instance where exception has to be tracked
        :param db: Database connection object for storing exception
        :param model: Database model object for tracking exception
        :param notifier: a notifier object that would notify notification to the subscribers
        :param recipients: list of recipients emails
        :param db_table_name: database table name in case if it's required overriding
        :param notification_subject_prefix: notification subject prefix
        :param url_prefix: URL prefix to be exposed by the web apps
        :param masking: a masking object or lambda function that can provide custom masking rules
        :param context_builder: a builder function that provides the request details,
        it can be used to provide custom data, apart from the default one
        :param ticketing:  a ticking mixing object used to create or update ticket in ticketing system
        """
        # Database related fields
        self.app = app
        self.db = db
        self.db_table = db_table_name
        self.model = model
        # masking related fields
        self.masking = masking
        # context builder object
        self.context_builder = context_builder
        self.views = None

        # notification related fields
        self.notifier = notifier
        self.notification_subject_prefix = notification_subject_prefix
        self.send_notification = False
        self.recipients = recipients
        self.notification_sender = None
        self.ticketing = ticketing

        self.active = False
        if self.app:
            self.init_app(app, db, model=model, notifier=notifier, url_prefix=url_prefix,
                          masking=masking, context_builder=context_builder,
                          ticketing=ticketing)

    def init_app(self, app, db, model=None, notifier=None, url_prefix=None, masking=None,
                 context_builder=defaults.DefaultContextBuilder(), ticketing=None):
        """
        Initialize this app with different attributes
        :param app: a Flask app instance
        :param db: Database connection object
        :param model: Database model class
        :param notifier: notifier app which will be used to notify notification
        :param url_prefix: Url prefix for WEB UI
        :param masking: a masking interface object or lambda function
        :param context_builder: a builder function that provides the request details,
        it can be used to provide custom data, apart from the default one
        :param ticketing :   a ticking mixing object used to create or update ticket in ticketing system
        :return: None
        """
        if self.active:
            raise ConfigError("App is already configured")
        self.app = app
        self.db = db
        if app is None:
            raise ConfigError("app is None")
        if model is None and self.db is None:
            raise ConfigError("Either db or model must be provide")

        send_notification = self.app.config.setdefault('APP_ERROR_SEND_NOTIFICATION',
                                                       defaults.APP_ERROR_SEND_NOTIFICATION)
        recipients = self.app.config.setdefault('APP_ERROR_RECIPIENT_EMAIL',
                                                defaults.APP_ERROR_RECIPIENT_EMAIL)
        subject_prefix = self.app.config.setdefault('APP_ERROR_SUBJECT_PREFIX',
                                                    defaults.APP_ERROR_SUBJECT_PREFIX)
        mask_with = self.app.config.setdefault('APP_ERROR_MASK_WITH', defaults.APP_ERROR_MASK_WITH)
        mask_key_has = self.app.config.setdefault('APP_ERROR_MASKED_KEY_HAS',
                                                  defaults.APP_ERROR_MASKED_KEY_HAS)
        url_prefix = url_prefix or self.app.config.setdefault('APP_ERROR_URL_PREFIX',
                                                              defaults.APP_ERROR_URL_PREFIX)
        self.notification_sender = self.app.config.setdefault('APP_ERROR_EMAIL_SENDER',
                                                              defaults.APP_ERROR_EMAIL_SENDER)

        global page_size
        self.model = model or self._get_model()
        self.views = Views(self.app, self.model, url_prefix)
        page_size = self.app.config.setdefault("APP_DEFAULT_LIST_SIZE", defaults.APP_DEFAULT_LIST_SIZE)
        # masking object setting
        if type(mask_key_has) == str:
            mask_key_has = (mask_key_has,)
        if mask_key_has and mask_with:
            self.masking = masking or Masking(mask_with, mask_key_has)

        self.notifier = notifier or getattr(app, "notifier", None) or getattr(app, "mailer", None)
        if self.notifier is not None and send_notification:
            if recipients not in [None, ""]:
                self.send_notification = True
                self.recipients = recipients
                if type(self.recipients) == str:
                    self.recipients = [self.recipients]
                if self.notification_sender is None:
                    raise ConfigError(
                        "Email recipients is set but notification sender is"
                        " not configured. set APP_ERROR_EMAIL_SENDER in app config")
                self.recipients = list(self.recipients)
            else:
                warn("APP_ERROR_RECIPIENT_EMAIL is not set in the app config")

            if subject_prefix in [None, ""]:
                warn("APP_ERROR_SUBJECT_PREFIX is not set in the app config")

        # Use the new style teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)
        self.context_builder = context_builder
        self.ticketing = ticketing
        self.active = True

    def teardown(self, exception):
        pass

    def _get_model(self):
        """
        :return: Default model for storing exception
        """

        class AppDbModel(ModelMixin, self.db.Model):
            db = self.db
            hash = Column(String(64), primary_key=True)
            host = Column(String(2048))
            path = Column(String(512))
            method = Column(String(32))
            request_data = Column(Text)
            exception_name = Column(String(256))
            traceback = Column(Text)
            count = Column(Integer, default=1)
            created_on = Column(DateTime)
            last_seen = Column(DateTime)

            def __repr__(self):
                return "AppDbModel(%s)" % self.__str__()

            @classmethod
            def delete(cls, rhash):
                """
                :param rhash: lookup key
                :return: None
                """
                cls.query.filter_by(hash=rhash).delete()
                cls.db.session.commit()

            @classmethod
            def create_or_update(cls, rhash, host, path, method, request_data,
                                 exception_name, traceback):
                try:
                    error = cls.query.filter_by(hash=rhash).one()
                    error.count += 1
                    error.last_seen = datetime.datetime.now()
                    # error.exception = exception
                    cls.db.session.commit()
                except NoResultFound:
                    now = datetime.datetime.now()
                    error = cls(hash=rhash, host=host, path=path, method=method,
                                request_data=str(request_data),
                                exception_name=exception_name, traceback=traceback,
                                created_on=now,
                                last_seen=now)
                    cls.db.session.add(error)
                    cls.db.session.commit()
                return error

            @classmethod
            def get_exceptions_per_page(cls, page_number=1):
                return cls.query.order_by(desc(cls.last_seen)).paginate(
                    page_number, page_size, False)

            @classmethod
            def get(cls, rhash):
                """
                :param rhash: key for lookup
                :return: Single entry of this class
                """
                error = cls.query.filter_by(hash=rhash).first()
                return error

            class Meta:
                table_name = self.db_table

        return AppDbModel

    def _send_notification(self, url, method, message, exception, error):
        if self.notification_subject_prefix:
            subject = "[%s][%s] %s" % (self.notification_subject_prefix, method, url)
        else:
            subject = "[%s] %s" % (method, url)
        if exception:
            subject = "[%s] %s" % (exception, subject)

        msg = Message(body=message, subject=subject, recipients=self.recipients,
                      sender=self.notification_sender)
        self.notifier.notify(msg, error)

    def _post_process(self, frame_str, frames, error):
        if self.send_notification:
            message = ('URL: %s' % request.path) + '\n\n'
            message += frame_str
            self._send_notification(request.url, request.method, message,
                                    frames[-1][:-1], error)
        if self.ticketing is not None:
            self.ticketing.raise_ticket(error)

    @staticmethod
    def _get_exception_name(o):
        return str(o).replace("'>", "").replace("<class '", "")

    def record_exception(self):
        """
        Record occurred exception, check whether the exception recording is
        enabled or not. If it's enabled then record all the details and store
        them in the database, it will notify email as well. The id of exception
        is SHA256 of frame string
        :return: None
        """
        if not self.active:
            return
        path = request.path
        host = request.host_url
        method = request.method
        ty, val, tb = sys.exc_info()
        frames = traceback.format_exception(ty, val, tb)
        traceback_str = format_exception(tb, masking=self.masking)
        frame_str = ''.join(frames)
        rhash = sha256(str.encode(frame_str, "UTF-8")).hexdigest()
        request_data = self.context_builder.get_context(request, masking=self.masking)
        error = self.model.create_or_update(rhash, host, path, method, str(request_data),
                                            self._get_exception_name(ty),
                                            traceback_str)
        self._post_process(frame_str, frames, error)

    def track_exception(self, func):
        """
        Decorator to be used for automatic exception capture
        """

        def wrapper(e):
            self.record_exception()
            return func(e)

        return wrapper

    def get_exceptions(self, page_number=1):
        """
        Get list of exception objects from persistence store
        :param page_number: documents of a specific page
        :return: list of exception objects
        """
        if self.model:
            return self.model.get_exceptions_per_page(page_number=page_number).items
        raise ConfigError

    def get_exception(self, rhash):
        """
        Get a specific exception, can be used for some customization etc
        :param rhash:  hash of the exception
        :return:  exception object
        """
        if self.model:
            return self.model.get(rhash)
        raise ConfigError

    def delete_exception(self, rhash):
        """
        Delete a specific exception from database
        :param rhash: hash of the exception
        :return:   whatever model returns
        """
        if self.model:
            return self.model.delete(rhash)
        raise ConfigError

    def create_or_update_exception(self, rhash, host, path, method, request_data,
                                   exception_name, traceback):
        if self.model:
            return self.model.create_or_update(rhash, host, path, method, request_data,
                                               exception_name, traceback)
        raise ConfigError
