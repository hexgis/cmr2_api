from django.db import models
from .critics_and_suggestions.models import *

class Institutions(models.Model):
    name = models.CharField(
        max_length=255
    )
    type = models.CharField(
        max_length=255
    )

    class Meta:
        app_label='admin_panel'
        verbose_name='institution'
        verbose_name_plural='institutions'

