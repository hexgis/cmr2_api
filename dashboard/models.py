from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
User = get_user_model()


class DashboardData(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dashboard_data',
    )

    last_date_login = models.DateTimeField(
        _('Data Último Login'),
        blank=False,
        null=False,
    )

    location = models.CharField(
        _('Localização'),
        max_length=255
    )
    ip = models.CharField(
        _('IP'),
        max_length=255
    )
    type_device = models.CharField(
        max_length=255,
    )
    browser = models.CharField(
        max_length=255
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        app_label = 'dashboard'
        verbose_name = 'Dashboard Data'
        ordering = ('-last_date_login', )
