from django.contrib import admin
from user_profile import models
from cmr2_api.mixins import AdminPermissionMixin

class UserSettingsAdmin(AdminPermissionMixin, admin.ModelAdmin):
    """
    Admin interface configuration for user settings management.

    Attributes:
    - list_display: Fields displayed in the list view of user settings.
    - fields: Fields editable in the admin interface for user settings.
    - search_fields: Fields searchable in the admin interface for user settings.

    """
    list_display = (
        'user',
        'dark_mode_active',
        'drawer_open_on_init',
        'interest_area_zoom_on_init',
        'map_zoom_buttons_visible',
        'map_initial_area_visible',
        'map_zoom_to_point_visible',
        'map_file_loader_visible',
        'map_draw_button_visible',
        'map_opacity_button_visible',
        'map_reachability_button_visible',
        'map_my_location_visible',
        'map_search_button_visible',
        'map_scale_visible',
        'minimap_visible',
        'map_pointer_coordinates_visible',
        'initial_extent',
    )

    fields = list_display
    search_fields = list_display

admin.site.register(models.UserSettings, UserSettingsAdmin)
