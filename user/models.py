import os
import unicodedata
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from permission import models as permission_models
from django.contrib.gis.db import models as gis_models
import uuid
from django.utils import timezone
from django.contrib.gis.db import models
from datetime import datetime


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

    INSTITUTION_TYPES = [
        ('FUNAI Sede', 'FUNAI Sede'),
        ('Coordenação Regional', 'Coordenação Regional'),
        ('Outros', 'Outros'),
    ]

    name = models.CharField(
        max_length=255,
        help_text=_('Institution')
    )

    acronym = models.CharField(
        max_length=20,
        help_text=_('Acronym'),
        null=True,
        blank=True,
    )

    institution_type = models.CharField(
        max_length=128,
        help_text=_('Type'),
        choices=INSTITUTION_TYPES,
        null=True,
        blank=True,
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
    is_active = models.BooleanField(default=True)

    avatar_blob = models.BinaryField(blank=True, null=True)

    dark_mode_active = models.BooleanField(
        default=False,
        null=True,
        blank=True
    )

    password = models.CharField(max_length=128, null=True, blank=True)

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


def rename_access_file(instance, filename):
    """
    Generates a consistent filename for the uploaded attachment.
    Replaces spaces and special characters in `instance.name`.
    """
    ext = filename.split('.')[-1]
    date_str = datetime.now().strftime('%Y-%m-%d')
    normalized_name = (
        unicodedata.normalize('NFKD', instance.name)
        .encode('ascii', 'ignore')
        .decode('ascii')
        .replace(' ', '_')
    )
    new_filename = f"solicitacao_acesso_{normalized_name}_{date_str}.{ext}"
    return os.path.join('attachments/access_request', new_filename)


class AccessRequest(models.Model):
    """
    Model for storing user requests to access restricted modules or areas.
    """
    class StatusType(models.IntegerChoices):
        PENDENTE = 1, 'Pendente'
        CONCEDIDA = 2, 'Concedida'
        RECUSADA = 3, 'Recusada'
        PENDENTE_COORD = 4, 'Pendente Coordenador'

    name = models.CharField(
        max_length=255,
        help_text=_("Name of the requester")
    )

    email = models.EmailField(
        help_text=_("Email of the requester")
    )

    department = models.CharField(
        max_length=255,
        help_text=_("Department of the requester")
    )

    user_siape_registration = models.IntegerField(
        help_text=_("SIAPE registration of the requester")
    )

    coordinator_name = models.CharField(
        max_length=255,
        help_text=_("Name of the coordinator")
    )
    coordinator_email = models.EmailField(

        help_text=_("Email of the coordinator")
    )

    coordinator_department = models.CharField(
        max_length=255,
        help_text=_("Department of the coordinator")
    )

    coordinator_siape_registration = models.IntegerField(
        help_text=_("SIAPE registration of the coordinator")
    )

    attachment = models.FileField(
        upload_to=rename_access_file,
        null=True,
        blank=True,
        help_text=_("Optional file with further details")
    )

    status = models.IntegerField(
        choices=StatusType.choices,
        default=StatusType.PENDENTE_COORD,
        help_text=_("Current status of the access request")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Timestamp when the request was created")
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "Timestamp when the request was reviewed (approved or denied)")
    )

    reviewed_by = models.ForeignKey(
        'user.User',
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        help_text=_("User who reviewed this request")
    )

    denied_details = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Details or reason for denial (if status=Recusada)")
    )

    class Meta:
        app_label = 'user'
        verbose_name = 'Access Request'
        verbose_name_plural = 'Access Requests'

    def __str__(self):
        return f"AccessRequest #{self.pk} - {self.name}"

    def approve(self, reviewer):
        """
        Marks this request as CONCEDIDA and sets reviewer fields.
        """
        self.status = self.StatusType.CONCEDIDA
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.denied_details = None
        self.save()

    def reject(self, reviewer, denied_reason=None):
        """
        Marks this request as RECUSADA and sets reviewer fields, reason, etc.
        """
        self.status = self.StatusType.RECUSADA
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.denied_details = denied_reason
        self.save()
