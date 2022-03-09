from django.db import models
from django.utils.translation import gettext_lazy as _
# project imports
from utils.core.models import TimeStampable
from apps.operations.constants import IntrestredInTraining


class TrainingForm(TimeStampable):
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=64)
    
    email_id = models.EmailField(verbose_name=_("Email address"), max_length=256, unique=True)
    
    phone_number = models.CharField(verbose_name=_("Phone"), max_length=16, unique=True)
    
    interested_in_training = models.CharField(
        verbose_name=_("If you are not eligible are you interested in training?"), 
        choices=IntrestredInTraining.choices, 
        max_length=64
    )
    
    class Meta:
        verbose_name = _("Training Information")
        verbose_name_plural = _("Training Information")
        ordering = ("-id",)

    def __str__(self):
        return f'{self.full_name}'
