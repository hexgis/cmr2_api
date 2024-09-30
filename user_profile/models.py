from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

from authorization import models as authorization_model
from admin_panel import models as admin_model

import os
from datetime import datetime

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

    dark_mode_active = models.BooleanField(
        default=False
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

    properties = models.JSONField(
        null=True,
        blank=True
    )

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


class UserUploadedFileGeometry(models.Model):
    """Model to store user uploaded file geometries.

    * Association:
        * Has one :model:`user_profile.UserUploadedFile`
    """

    user_uploaded = models.ForeignKey(
        UserUploadedFile,
        on_delete=models.CASCADE,
        related_name='user_uploaded_file',
    )

    geom = models.GeometryField(srid=4326) 

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of UserUploadedFileGeometry model.
        """
        return f'{self.id}: {self.user_uploaded}'

    class Meta:
        app_label = 'user_profile'
        verbose_name = 'User Uploaded File - Geometry'
        verbose_name_plural = 'User Uploaded Files - Geometries'
        ordering = ('user_uploaded', )

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        app_label = 'user_profile'
        verbose_name = 'password_reset_code'

class UserPermission(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING
        )
    
    permission = models.ForeignKey(
        authorization_model.PermissionsList,
        on_delete=models.DO_NOTHING
    )

    class Meta:
        app_label = 'user_profile'
        verbose_name = 'user_permission_list'

class UserData(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING
    )
    # institution = models.OneToOneField(
    #     admin_model.Institutions,
    #     on_delete=models.DO_NOTHING
    # )

    # data_request_access = models.ForeignKey(
    #   AccessRequest
    # )

    class Meta:
        app_label='user_profile'
        verbose_name='user data'
        verbose_name_plural='users datas'

def rename_file(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"solicitacao_acesso_{instance.name}_{datetime.now().strftime('%Y-%m-%d')}.{ext}"
    return os.path.join('attachments', new_filename)

class AccessRequest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    department = models.CharField(max_length=255)
    user_siape_registration = models.IntegerField()
    coordinator_name = models.CharField(max_length=255)
    coordinator_email = models.EmailField()
    coordinator_department = models.CharField(max_length=255)
    coordinator_siape_registration = models.IntegerField()
    attachment = models.FileField(upload_to=rename_file, null=True, blank=True)
    status = models.BooleanField(
        default=False
    )
    dt_solicitation = models.DateTimeField(auto_now_add=True) 
    dt_approvement = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label='user_profile'
        verbose_name='Access Request'
        verbose_name_plural='Access Requests'
