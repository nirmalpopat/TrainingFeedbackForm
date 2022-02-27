# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    """bad request error"""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"


class NotFoundException(APIException):
    """bad found error"""

    status_code = status.HTTP_404_NOT_FOUND
    default_code = "error"


class NotAllowedException(APIException):
    """not allowed error"""

    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_code = "error"


class NotAcceptableException(APIException):
    """not acceptable error"""

    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_code = "error"


class InternalErrorException(APIException):
    """internal server error """

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"
