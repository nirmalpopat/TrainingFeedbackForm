# -*- coding: utf-8 -*-
# python imports
from __future__ import unicode_literals

# lib imports
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import TextChoices
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# project imports
from apps.accounts.managers.user import UserManager, UserQuerySet


def activation_token():
    return str(abs(hash(f"{uuid.uuid4()}")) % (10 ** 4))


class UserTypeChoice(TextChoices):
    STUDENT = _("student")
    TEACHER = _("teacher")


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model
    """
    username = models.CharField(verbose_name=_("Username"), max_length=256, unique=True)
    phone = models.CharField(verbose_name=_("Phone"), max_length=128, unique=True)
    name = models.CharField(verbose_name=_("First Name"), max_length=128)
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user \
            can log into this admin site."
        ),
    )
    user_type = models.CharField(verbose_name=_("User type"), choices=UserTypeChoice.choices, max_length=10)
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=_(
            "Designates whether this user \
            should be treated as active. \
            Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(verbose_name=_("date joined"), default=timezone.now)
    otp = models.CharField(verbose_name="OTP", max_length=6, default=activation_token)
    classroom_link = models.URLField(null=True, blank=True)

    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "phone"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        indexes = [models.Index(fields=["username", "phone"])]
        ordering = ("-id",)

    @property
    def is_teacher(self):
        return self.user_type == UserTypeChoice.TEACHER

    @property
    def is_student(self):
        return self.user_type == UserTypeChoice.STUDENT

    def __unicode__(self):
        return f"{self.username} - {self.name}"

    def __str__(self):
        return f"{self.username} - {self.name}"
