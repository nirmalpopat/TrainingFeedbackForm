from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class IntrestredInTraining(TextChoices):
    YES = "yes", _("Yes")
    NO = "no", _("No"),
    MAY_BE = "may_be", _("May Be")