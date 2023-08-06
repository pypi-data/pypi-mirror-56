# -*- coding: utf-8 -*-
#
#     Exception formatter utils module
#
#     :copyright: 2018 Sonu Kumar
#     :license: BSD-3-Clause
#

import six
from .mixins import MaskingMixin


class Masking(MaskingMixin):
    """
    A simple function like class used for masking rule.
    """

    def __call__(self, key):
        if isinstance(key, six.string_types):
            tmp_key = key.lower()
            for k in self.mask_key_has:
                if k in tmp_key:
                    return True, "'%s'" % self.mask_with
        return False, None


class ConfigError(Exception):
    """
    A error class which will be raised by the app if it's not configure properly
    """
    pass
