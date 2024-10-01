from django.contrib import admin
from deter_monitoring import models
from cmr2_api.mixins import AdminPermissionMixin

class DeterTIAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """Django administrator for `models.DeterTI` data."""

    # Fields to be displayed in the admin list view
    list_display = (
        'ds_cr',          # Display string for the Deter TI
        'no_ti',          # Name of the TI
        'classname',      # Class name
        'quadrant',       # Quadrant information
        'path_row',       # Path row information
        'areatotalkm',    # Total area in km²
        'view_date',      # View date
        'sensor',         # Sensor used
        'satellite',      # Satellite information
        'uf',             # Federal unit
        'municipality',   # Municipality
        'uc',             # Conservation unit
    )

    # Fields to be displayed in the admin detail view
    field = list_display

    # Fields to be used in the admin search functionality
    search_fields = list_display

# Register the admin class with the associated model
admin.site.register(models.DeterTI, DeterTIAdmin)
