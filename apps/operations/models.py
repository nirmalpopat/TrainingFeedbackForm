from django.db import models
from django.utils.translation import gettext_lazy as _
# project imports
from utils.core.models import TimeStampable
from apps.operations.constants import IntrestredInTraining
# Create your models here.

class TrainingInformations(TimeStampable):
    full_name = models.CharField(verbose_name=_("Full Name"), max_length=64)
    
    email_id = models.EmailField(verbose_name=_("Email address"), max_length=256)
    
    phone_number = models.CharField(verbose_name=_("Phone"), max_length=16)
    
    intrested_in_training = models.CharField(
        verbose_name=_("If you are not eligible are you interested in training?"), 
        choices=IntrestredInTraining.choices, 
        max_length=64
    )
    
    class Meta:
        verbose_name = _("Training Information")
        verbose_name_plural = _("Training Informations")
        indexes = [models.Index(fields=["intrested_in_training"])]
        ordering = ("-id",)

    def __str__(self):
        return f'{self.full_name}'