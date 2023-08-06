# -*- coding: utf-8 -*-
#
#    Exception formatter mixin classes
#
#    :copyright: 2018 Sonu Kumar
#    :license: BSD-3-Clause
#


class MaskingMixin(object):

    def __init__(self, mask_with, mask_key_has):
        """
        :param mask_with: masked value to be used for a given variable
        :param mask_key_has: tuple of strings to be used for checking masking rule
        """
        self.mask_key_has = mask_key_has
        self.mask_with = mask_with

    def __call__(self, key):
        raise NotImplementedError


class ModelMixin(object):
    """
    Base interface for data mode which can be used to store data in MongoDB/MySQL or any other data store.
    """
    hash = None
    host = None
    path = None
    method = None
    request_data = None
    exception_name = None
    traceback = None
    count = None
    created_on = None
    last_seen = None

    def __str__(self):
        return "'%s' '%s' %s" % (self.host, self.path, self.count)

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return "ModelMixin(%s)" % self.__str__()

    @classmethod
    def delete(cls, rhash):
        """
        :param rhash: lookup key
        :return: None
        """
        raise NotImplementedError

    @classmethod
    def create_or_update(cls, rhash, host, path, method, request_data,
                         exception_name, traceback):
        """
        :param rhash: Key of the db entry
        :param host: App host e.g. example.com
        :param path: request path
        :param method: request method (GET/POST/PUT etc)
        :param request_data: request form data
        :param exception_name: exception name
        :param traceback: Exception data captured
        :return:  error model object
        """
        raise NotImplementedError

    @classmethod
    def get_exceptions_per_page(cls, page_number=1):
        """
        An object having these properties,
        has_next, next_num, has_prev, prev_num and items
        on the returned object like SQLAlchemy's Pagination
        :return: a paginated object
        """
        raise NotImplementedError

    @classmethod
    def get(cls, rhash):
        """
        :param rhash: key for lookup
        :return: Single entry of this class
        """
        raise NotImplementedError


class NotificationMixin(object):
    """
    A notification mixin class which can be used to notify any kind of notification.
    """

    def __init__(self, *args, **kwargs):
        pass

    def notify(self, message, exception):
        """
        :param message: message is object of email instances Message from flask email
        :param exception : exception model object
        :return: None
        """
        raise NotImplementedError


class ContextBuilderMixin(object):
    """
    A context builder mixing that can be used to provide custom context details.
    This will provide entire details, that would be used for DB logging
    for usage see default context builder DefaultContextBuilder
    """

    def __init__(self, *args, **kwargs):
        pass

    def get_context(self, request, masking=None):
        raise NotImplementedError


class TicketingMixin(object):
    """
    A mixing class that would be called with model object to raise the ticket.
    It can be used to directly create or update ticket in ticketing system
    """

    def __init__(self, *args, **kwargs):
        pass

    def raise_ticket(self, exception):
        """
        :param exception: exception model object
        :return: None
        """
        raise NotImplementedError
