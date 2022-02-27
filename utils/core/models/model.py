# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampable(models.Model):
    """
    Record timestamps of a Content.
    * Model instance is never deleted, its marked as deleted with is_deleted.
    """

    create_date = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name=_("Modified At"), auto_now=True)

    class Meta:
        abstract = True
