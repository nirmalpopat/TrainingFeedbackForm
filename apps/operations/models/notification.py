from django.db import models
from django.utils.translation import gettext_lazy as _
# project imports
from utils.core.models import TimeStampable


class NotificationTemplate(TimeStampable):
    """
    Description of NotificationTemplate Model
    """
    
    name = models.CharField(verbose_name=_("Notification template name"), max_length=64)
    subject = models.TextField(verbose_name=_("Notification Subject"))
    content = models.TextField(verbose_name=_("Notification Content"))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
