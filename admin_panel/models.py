from django.db import models

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

