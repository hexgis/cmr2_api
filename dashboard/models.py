from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

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

    class Meta:
        app_label = 'dashboard'
        verbose_name = 'Dashboard Data'
        ordering = ('-last_date_login', )
