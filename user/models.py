from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from permission import models as permission_models
from django.contrib.gis.db import models as gis_models
import uuid
from django.utils import timezone
from django.contrib.gis.db import models
from datetime import datetime
import os


class Group(models.Model):
    """Model to store group informatio.

    * Association:
        * Has many :model:`catalog.Image`
        * Has many :model:`catalog.Satellite`
    """

    name = models.CharField(max_length=50)

    description = models.CharField(max_length=255)

    layer_permissions = models.ManyToManyField(
        permission_models.LayerPermission,
        related_name='groups',
        blank=True
    )

    component_permissions = models.ManyToManyField(
        permission_models.ComponentPermission,
        related_name='groups',
        blank=True
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Group model.
        """

        return f'{self.name} | {self.description}'

    class Meta:
        """Meta class for Group model."""

        app_label = 'user'


class Institution(models.Model):
    """Model to store all Institutions.

    * Association:
        * Has one :model:`user.Institution`
    """

    name = models.CharField(
        max_length=255,
        help_text=_('Institution')
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Institution model.
        """

        return f'{self.name}'

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'


class Role(models.Model):
    """Model to store role information.

    * Association:
        * Has many :model:`Group`
    """

    name = models.CharField(max_length=50)

    description = models.CharField(max_length=255)

    groups = models.ManyToManyField(
        Group,
        related_name='roles',
    )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of Role model.
        """

        return f'{self.name} | {self.description}'

    class Meta:
        """Meta class for Role model."""

        app_label = 'user'


class User(AbstractUser):

    email = models.EmailField(
        _('email address'),
        unique=True
    )

    roles = models.ManyToManyField(
        Role,
        related_name='users',
        blank=True
    )

    institution = models.ForeignKey(
        Institution,
        help_text=_('User institution'),
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    avatar = models.FileField(
        _('Avatar'),
        blank=True,
        null=True,
    )

    token = models.TextField(
        _('Token'),
        blank=True,
        null=True,
    )

    avatar_blob = models.BinaryField(blank=True, null=True)

    dark_mode_active = models.BooleanField(
        default=False
    )

    class Meta:
        """Meta class for User model."""

        app_label = 'user'
        db_table = 'user'

    def is_admin(self) -> bool:
        """Verify if user has admin role or is a superuser.

        Returns:
            bool: Returns True if user is admin or False otherwise.
        """

        return self.roles.filter(name='admin').exists() or self.is_superuser

    def save(self, *args, **kwargs):
        """Validate and save the file."""

        self.full_clean()
        super(User, self).save(*args, **kwargs)

        super().save()

    def __str__(self) -> str:
        """CustomUser model data.

        Returns:
            str: Email or username.
        """

        return f"{self.email or self.username}"


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

    class Meta:
        """Meta class for UserUploadedFile model."""

        app_label = 'user'
        db_table = 'user_upload_file'
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'
        ordering = ('-user', )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of UserUploadedFile model.
        """

        return f'{self.user}: {self.name}'


class UserUploadedFileGeometry(models.Model):
    """Model to store user uploaded file geometries.

    * Association:
        * Has one :model:`user.UserUploadedFile`
    """

    user_uploaded = models.ForeignKey(
        UserUploadedFile,
        on_delete=models.CASCADE,
        related_name='user_uploaded_file',
    )

    geom = models.GeometryField(srid=4326)

    properties = models.JSONField(
        null=True,
        blank=True
    )

    class Meta:
        """Meta class for UserUploadedFileGeometry model."""

        app_label = 'user'
        db_table = 'user_uploaded_file_geometry'
        verbose_name = 'Uploaded File - Geometry'
        verbose_name_plural = 'Uploaded Files - Geometries'
        ordering = ('user_uploaded', )

    def __str__(self):
        """Model class string.

        Returns:
            str: short description of UserUploadedFileGeometry model.
        """
        return f'{self.id}: {self.user_uploaded}'


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        app_label = 'user'
        verbose_name = 'password_reset_code'


class AccessRequest(models.Model):
    """
        Represents a user's request for access to restricted modules or areas.

        Each request is associated with a user and records relevant details such as
        the user's institution, department, and the approval status of the request.

        Fields:
            user (ForeignKey): The user making the request.
            institution (ForeignKey): The institution associated with the request.
            user_siape_registration (IntegerField): SIAPE registration of the user.
            coordinator_name (CharField): Name of the user's coordinator.
            coordinator_email (EmailField): Email address of the user's coordinator.
            coordinator_department (CharField): Department of the coordinator.
            coordinator_siape_registration (IntegerField): SIAPE registration of the coordinator.
            attachment (FileField): Optional file attachment related to the request.
            status (BooleanField): Indicates whether the request is approved (True) or pending (False).
            dt_solicitation (DateTimeField): Timestamp when the request was created.
            dt_approvement (DateTimeField): Timestamp when the request was approved.

        Meta:
            app_label (str): Application label for the model.
            verbose_name (str): Singular name for the model in admin interfaces.
            verbose_name_plural (str): Plural name for the model in admin interfaces.
        """

    def rename_file(instance, filename):
        ext = filename.split('.')[-1]
        new_filename = f"solicitacao_acesso_{instance.name}_{datetime.now().strftime('%Y-%m-%d')}.{ext}"
        return os.path.join('attachments/access_request', new_filename)

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='access_requests',
        help_text='Usuário que solicita acesso'
    )

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='access_requests',
    )

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
        app_label = 'user'
        verbose_name = 'Access Request'
        verbose_name_plural = 'Access Requests'
