# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
from rest_framework.permissions import BasePermission


class IsAuthenticatedStudent(BasePermission):
    """
    Allows access only to authenticated student users
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_student)


class IsAuthenticatedCompany(BasePermission):
    """
    Allows access only to authenticated company users
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_company)

