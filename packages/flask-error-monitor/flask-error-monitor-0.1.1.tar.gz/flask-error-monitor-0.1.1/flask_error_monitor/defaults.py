# -*- coding: utf-8 -*-
#
#    Flask error monitor app's default value and class
#
#    :copyright: 2018 Sonu Kumar
#    :license: BSD-3-Clause
#


from flask_error_monitor.mixins import ContextBuilderMixin

APP_ERROR_SEND_NOTIFICATION = False
APP_ERROR_RECIPIENT_EMAIL = None
APP_ERROR_SUBJECT_PREFIX = ""
APP_ERROR_MASK_WITH = "**************"
APP_ERROR_MASKED_KEY_HAS = ("password", "secret")
APP_ERROR_URL_PREFIX = "/dev/error"
APP_ERROR_EMAIL_SENDER = None
APP_DEFAULT_LIST_SIZE = 20


class DefaultContextBuilder(ContextBuilderMixin):
    """
    Default request builder, this records, form data, header and URL parameters and mask them if necessary
    """

    def get_context(self, request, masking=None):
        form = dict(request.form)
        headers = dict(request.headers)
        if masking:
            for key in form:
                masked, value = masking(key)
                if masked:
                    form[key] = value
            for key in headers:
                masked, value = masking(key)
                if masked:
                    headers[key] = value

        request_data = str({
            'headers': headers,
            'args': dict(request.args),
            'form': form
        })
        return request_data
