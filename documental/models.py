from django.db import models

from django.utils.translation import ugettext_lazy as _


class DocsAction(models.Model):
    """DocsAction model data for documental model."""

    id_action = models.IntegerField(
        _('Action Identifier'),
        unique=True,
    )

    no_action = models.CharField(
        _('Action name'),
        max_length=255,
        unique=True,
    )

    dt_creation = models.DateTimeField(
        _('Registration date'),
        null=True,
        blank=True,
    )

    action_type = models.CharField(
        _('Type of action'),
        max_length=255,
        null=True,
        blank=True,
    )

    action_type_group = models.CharField(
        _('Group within action types'),
        max_length=255,
        null=True,
        blank=True,
    )

    description = models.CharField(
        _('Description of action'),
        max_length=512,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.DocsAction` model."""
        ordering = ['action_type']
        app_label = 'documental'
        verbose_name = 'Document Action'
        verbose_name_plural = 'Documents Actions'


class UsersCMR(models.Model):
    """UsersCMR model data for documental model."""

    id_user = models.IntegerField(
        _('User Identifier'),
        unique=True,
    )

    first_name = models.CharField(
        _('Name of who registered'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.UsersCMR` model."""
        app_label = 'documental'
        verbose_name = 'User CMR'
        verbose_name_plural = 'Users CMR'
        # db_table = 'painel\".\"auth_user'
        # managed = False


class DocumentalDocs(models.Model):
    """DocumentalDocs model data for documental model."""

    id_document = models.IntegerField(
        _('Key Identifier'),
        null=False,
        blank=False,
    )

    path_document = models.CharField(
        _('Document file path'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_document = models.CharField(
        _('Document name'),
        max_length=255,
        null=True,
        blank=True,
    )

    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    usercmr_id = models.ForeignKey(
        'documental.UsersCMR',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    st_available = models.BooleanField(
        _('Document available'),
        default=False,
        null=True,
        blank=True,
    )

    st_excluded = models.BooleanField(
        _('Deleted document'),
        default=False,
        null=True,
        blank=True,
    )

    dt_registration = models.DateTimeField(
        _('Document registration date'),
        null=True,
        blank=True,
    )

    dt_update = models.DateTimeField(
        _('Last update date'),
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
        _('Funai code - Indigenous Lands'),
        null=True,
        blank=True,
    )

    no_ti = models.CharField(
        _('Indigenous Lands name'),
        max_length=255,
        null=True,
        blank=True,
    )

    action_id = models.ForeignKey(
        'documental.DocsAction',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    co_cr = models.BigIntegerField(
        _('Regional Coordenation code'),
        blank=True,
        null=True,
    )

    ds_cr = models.CharField(
        _('Regional Coordenation name'),
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        """"Meta class for `documental.DocumentalDocs` model."""
        abstract = True
        ordering = ['-dt_registration']
        app_label = 'documental'
        verbose_name = 'Documental Doc'
        verbose_name_plural = 'Documental Docs'

    def __str__(self) -> str:
        """Returns `documental.DocumentalDocs` string data.

        Returns:
            str: model data path_documento.
        """
        return self.path_document


class DocsLandUser(DocumentalDocs):
    """DocsLandUser model data for documental model."""

    nu_year = models.IntegerField(
        _('Delivery reference year'),
        null=True,
        blank=True,
    )

    nu_year_map = models.IntegerField(
        _('Year of the map'),
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.UsersCMR` model."""
        app_label = 'documental'
        verbose_name = 'Document Land User'
        verbose_name_plural = 'Documents Land User'

    def __str__(self) -> str:
        """Returns `documental.DocsLandUser` string data.
        Returns:
            str: model data document name.
        """
        return self.no_document


class DocsDocumentTI(DocumentalDocs):
    """DocsDocumentTI model data for documental model."""

    dt_document = models.DateField(
        _('Date of document'),
        null=True,
        blank=True,
    )

    no_extension = models.CharField(
        _('Document extension'),
        max_length=255,
        null=True,
        blank=True,
    )

    file = models.FileField(
        _('Docs DocumentTI file path'),
        upload_to='DocumentTI/',
    )

    class Meta:
        """"Meta class for `documental.DocsDocumentTI` model."""
        app_label = 'documental'
        verbose_name = 'Document Indigenous Lands'
        verbose_name_plural = 'Documents Indigenous Lands'

    def __str__(self) -> str:
        """Returns `documental.DocsDocumentTI` string data.
        Returns:
            str: model data document name.
        """
        return self.no_document


class DocsMapoteca(DocumentalDocs):
    """DocsMapoteca model data for documental model."""

    no_description = models.CharField(
        _('File Description'),
        max_length=255,
        blank=True,
        null=True,
    )

    map_dimension = models.CharField(
        _('Map page dimension'),
        max_length=2,
        blank=True,
        null=True,
    )

    js_ti = models.CharField(
        _('Array de Terras Indígenas'),
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        """"Meta class for `documental.DocsMapoteca` model."""
        app_label = 'documental'
        verbose_name = 'Document Mapoteca'
        verbose_name_plural = 'Documents Mapoteca'

    def __str__(self) -> str:
        """Returns `documental.DocsMapoteca` string data.
        Returns:
            str: model data document name.
        """
        return self.no_document
