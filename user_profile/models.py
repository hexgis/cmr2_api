from django.contrib.gis.db import models
from django.contrib.auth.models import User


class UserSettings(models.Model):
    """Model to store user settings.

    * Association:
        * Has one :model:`django.contrib.auth.User`
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='settings',
        primary_key=True,
    )

    drawer_open_on_init = models.BooleanField(
        default=True
    )

    interest_area_zoom_on_init = models.BooleanField(
        default=True
    )

    map_zoom_buttons_visible = models.BooleanField(
        default=True
    )

    map_initial_area_visible = models.BooleanField(
        default=True
    )

    map_zoom_to_point_visible = models.BooleanField(
        default=True
    )

    map_file_loader_visible = models.BooleanField(
        default=True
    )

    map_draw_button_visible = models.BooleanField(
        default=True
    )

    map_opacity_button_visible = models.BooleanField(
        default=True
    )

    map_reachability_button_visible = models.BooleanField(
        default=True
    )

    map_my_location_visible = models.BooleanField(
        default=True
    )

    map_search_button_visible = models.BooleanField(
        default=True
    )

    map_scale_visible = models.BooleanField(
        default=True
    )

    minimap_visible = models.BooleanField(
        default=True
    )

    map_pointer_coordinates_visible = models.BooleanField(
        default=True
    )

    initial_extent = models.PolygonField(
        srid=4674,
        null=True,
        blank=True
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of model.
        """

        return f'Settings of user {self.user}'

    class Meta:
        app_label = 'user_profile'
        verbose_name = 'UserSettings'
        verbose_name_plural = 'UserSettings'
        ordering = ('-user', )


class UserUploadedFile(models.Model):
    """Model to store user uploaded files.

    * Association:
        * Has one :model:`django.contrib.auth.User`
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )

    name = models.CharField(max_length=255)

    date_created = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of UserUploadedFile model.
        """

        return f'{self.user}: {self.name}'

    class Meta:
        app_label = 'user_profile'
        verbose_name = 'User Uploaded File'
        verbose_name_plural = 'User Uploaded Files'
        ordering = ('-user', )
