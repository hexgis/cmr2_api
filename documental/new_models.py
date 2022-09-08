from django.db import models

from django.utils.translation import ugettext_lazy as _


class DocsAction(models.Model):
    """DocsAction model data for documental model."""

    id_action = models.IntegerField(
        _('Identifier Action'),
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

    description = models.CharField(
        _('Description of action'),
        max_length=512,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.DocsAction` model."""
        app_label = 'documental'
        verbose_name = 'Document Action'
        verbose_name_plural = 'Documents Actions'


class UsersCMR(models.Model):
    """UsersCMR model data for documental model."""

    id_user = models.IntegerField(
        _('Identifier User'),
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
        # usuario = models.ForeignKey(settings.AUTH_USER_MODEL, related_name=_('usuario'))
        # db_table = 'painel\".\"auth_user'
        # managed = False


class auth_institution_temp(models.Model):
    """Institution model data for documental model."""

    id_institution = models.IntegerField(
        _('Identifier institution'),
        unique=True,
    )

    name = models.CharField(
        _('Name institution'),
        max_length=255,
        unique=True,
        null=False,
    )

    institution_type = models.CharField(
        _('Type of institution'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.auth_institution_temp` model."""
        app_label = 'documental'
        verbose_name = 'Auth Institution Temp'
        verbose_name_plural = 'Auth Institutions Temp'
        ordering = ['-name']
        # db_table = 'painel\".\"auth_institution'
        # managed = False


class DocumentalDocs(models.Model):
    """DocumentalDocs model data for documental model."""

    id_document = models.IntegerField(
        _('Identifier key'),
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

    usercmr_id = models.ForeignKey(
        'documental.UsersCMR',
        on_delete=models.DO_NOTHING,
        related_name='documentosdocs_usercmr',
        null=True,
    )

    institution = models.ForeignKey(
        'documental.auth_institution_temp', 
        related_name=_('DocsMapoteca_institution'), 
        null=True,
        default=10
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
        _('Funai code - Indigenou Lands'),
        null=True,
        blank=True,
    )

    action_id = models.ForeignKey(
        'documental.DocsAction',
        on_delete=models.DO_NOTHING,
        related_name='documentosdocs_action',
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

    no_ti = models.CharField(
        _('Indigenou Lands name'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.DocsDocumentTI` model."""
        app_label = 'documental'
        verbose_name = 'Document Indigenou Lands'
        verbose_name_plural = 'Documents Indigenou Lands'

    def __str__(self) -> str:
        """Returns `documental.DocsDocumentTI` string data.
        Returns:
            str: model data document name.
        """
        return self.no_document


from django.contrib.postgres.fields.jsonb import JSONField
class DocsMapoteca(DocumentalDocs):
    """DocsMapoteca model data for documental model."""

    no_descricao = models.CharField(
        _('Descrição do arquivo'), 
        max_length=255,
    )

    formato = models.CharField(
        _('Formato do Mapa'),
        max_length=2,
    )
    
    js_ti = JSONField(
        _('Array de Terras Indígenas em formato JSON ex: [{\"no_ti\":\"Cachoeira Seca\"}]'),
        default=[],
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
