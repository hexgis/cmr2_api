from django.db import models

from django.utils.translation import ugettext_lazy as _


class DocsAction(models.Model):
    """DocsAction model data for documental model."""
    id = models.IntegerField(
        _('Action id key'),
        unique=True,
        primary_key=True,
    )

    no_acao = models.CharField(
        _('Action name'),
        max_length=255,
        unique=True,
    )

    dt_criacao = models.DateTimeField(
        _('Registration date'),
        null=True,
        blank=True,
    )

    descricao = models.CharField(
        _('Description of documental type'),
        max_length=512,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.DocsAction` model."""
        app_label = 'documental'
        verbose_name = 'Document Action'
        verbose_name_plural = 'Documents Actions'


class Usuario(models.Model):
    """Usuario model data for documental model."""

    id = models.IntegerField(
        _('User id key'),
        unique=True,
        primary_key=True,
    )

    first_name = models.CharField(
        _('Name of who registered'),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.Usuario` model."""
        app_label = 'documental'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        # db_table = 'painel\".\"auth_user'
        # managed = False


class Document(models.Model):
    class Meta:
        ordering = ['uploaded_at']

    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=False, null=False)
    # description
    data = models.CharField(max_length=200, blank=True, null=True)
    action = models.CharField(
        'Document action',
        max_length=200,
    )
    def __str__(self):
        return self.file.name


class DocumentalDocs(models.Model):
    """DocumentalDocs model data for documental model."""

    id = models.IntegerField(
        _('Primary key'),
        unique=True,
        primary_key=True,
    )

    path_documento = models.CharField(
        _('Document path'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_documento = models.CharField(
        _('Document name'),
        max_length=255,
        null=True,
        blank=True,
    )

    usuario_id = models.ForeignKey(
        'documental.Usuario',
        on_delete=models.DO_NOTHING,
        related_name='documentosdocs_usuario_id',
        null=True,
    )

    st_disponivel = models.BooleanField(
        _('Document available'),
        default=False,
        null=True,
        blank=True,
    )

    st_excluido = models.BooleanField(
        _('Deleted document'),
        default=False,
        null=True,
        blank=True,
    )

    dt_cadastro = models.DateTimeField(
        _('Document registration date'),
        null=True,
        blank=True,
    )

    dt_atualizacao = models.DateTimeField(
        _('Last update date'),
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
        _('Funai code - Indigenou Lands'),
        null=True,
        blank=True,
    )

    id_acao = models.ForeignKey(
        'documental.DocsAction',
        on_delete=models.DO_NOTHING,
        related_name='documentosdocs_action',
        null=True
    )

    no_extensao = models.CharField(
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

    co_cr = models.BigIntegerField(
        _('Regional Coordenation code'),
        blank=True,
        null=True
    )

    ds_cr = models.CharField(
        _('Regional Coordenation name'),
        max_length=255,
        blank=True,
        null=True
    )

    dt_documento = models.DateField(
        _('Date of document'),
        null=True,
        blank=True,
    )

    nu_ano = models.IntegerField(
        _('Delivery reference year'),
        null=True,
        blank=True,
    )

    nu_ano_mapa = models.IntegerField(
        _('Year of the map'),
        null=True,
        blank=True,
    )

    class Meta:
        """"Meta class for `documental.DocumentalDocs` model."""
        app_label = 'documental'
        verbose_name = 'Documental Doc'
        verbose_name_plural = 'Documental Docs'

    def __str__(self) -> str:
        """Returns `documental.DocumentalDocs` string data.

        Returns:
            str: model data path_documento.
        """
        return self.path_documento
