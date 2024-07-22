from django.contrib import admin
from cmr2_api.mixins import AdminPermissionMixin
from dashboard import models


# Register your models here.
class DashboardDataAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'last_date_login',
        'location',
        'ip'
    )

    search_fields = list_display
    list_filter = list_display
    fields = list_display

admin.site.register(models.DashboardData, DashboardDataAdmin)
