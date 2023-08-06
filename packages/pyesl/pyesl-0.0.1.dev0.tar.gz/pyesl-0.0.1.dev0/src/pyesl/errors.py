# -*- coding: utf-8 -*-

class BaseError(Exception):
    """
    Raised when a error occur.
    """

    SUBCODE = 10501
    STATUS = u'PyESL Error'

    def __init__(self, message="", subcode=SUBCODE, status=STATUS, *args, **kwargs):
        self.status = status or self.STATUS
        self.subcode = subcode or self.SUBCODE
        Exception.__init__(self, message, *args, **kwargs)


class ParamError(BaseError):
    SUBCODE = 10422
    STATUS = u'PyESL Invalid Parameter Error'

class DuplicateKeyError(BaseError):
    SUBCODE = 11061
    STATUS = u'PyESL Duplicate Key Error'