from django.contrib import admin
from cmr2_api.mixins import AdminPermissionMixin
from dashboard import models


# Register your models here.
class DashboardDataAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'last_date_login',
        'location',
        'ip',
        'type_device',
        'browser',
    )

    search_fields = list_display
    list_filter = (
        'last_date_login',
        'type_device',
        'browser'
    )
    fields = list_display

admin.site.register(models.DashboardData, DashboardDataAdmin)
