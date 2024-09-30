from django.db import models
from django.utils.translation import ugettext_lazy as _


class DocsAction(models.Model):
    """DocsAction model data for documental model."""

    id_action = models.IntegerField(
        _('Identificador da Ação'),
        unique=True,
    )

    no_action = models.CharField(
        _('Nome'),
        max_length=255,
        unique=True,
    )

    dt_creation = models.DateTimeField(
        _('Data de Registro'),
        null=True,
        blank=True,
    )

    action_type = models.CharField(
        _('Tipo de Ação'),
        max_length=255,
        null=True,
        blank=True,
    )

    action_type_group = models.CharField(
        _('Grupo com Tipos de Ação'),
        max_length=255,
        null=True,
        blank=True,
    )

    description = models.CharField(
        _('Descrição da Ação'),
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
        _('Identificador do Usuário'),
        unique=True,
    )

    first_name = models.CharField(
        _('Nome de quem se inscreveu'),
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
        _('Identificador Chave'),
        null=False,
        blank=False,
    )

    path_document = models.CharField(
        _('Caminho do arquivo do documento'),
        max_length=255,
        null=True,
        blank=True,
    )

    no_document = models.CharField(
        _('Nome do Documento'),
        max_length=255,
        null=True,
        blank=True,
    )

    usercmr_id = models.ForeignKey(
        'documental.UsersCMR',
        on_delete=models.DO_NOTHING,
        null=True,
    )

    st_available = models.BooleanField(
        _('Documento disponível'),
        default=False,
        null=True,
        blank=True,
    )

    st_excluded = models.BooleanField(
        _('Documento excluído'),
        default=False,
        null=True,
        blank=True,
    )

    dt_registration = models.DateTimeField(
        _('Data de registro do documento'),
        auto_now_add=True,
    )

    dt_update = models.DateTimeField(
        _('Data da última atualização'),
        auto_now=True,
    )

    co_funai = models.IntegerField(
        _('Código Funai – Terras Indígenas'),
        null=True,
        blank=True,
    )

    no_ti = models.CharField(
        _('Nome das Terras Indígenas'),
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
        _('Código de Coordenação Regional'),
        blank=True,
        null=True,
    )

    ds_cr = models.CharField(
        _('Nome da Coordenação Regional'),
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
        _('Ano de referência de entrega'),
        null=True,
        blank=True,
    )

    nu_year_map = models.IntegerField(
        _('Ano do mapa'),
        null=True,
        blank=True,
    )

    file = models.FileField(
        _('Caminho do arquivo'),
        upload_to='DocsLandUser/',
        default='Undefined File',
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
        _('Data do documento'),
        null=True,
        blank=True,
    )

    no_extension = models.CharField(
        _('Extensão do documento'),
        max_length=255,
        null=True,
        blank=True,
    )

    file = models.FileField(
        _('Caminho do Arquivo'),
        upload_to='DocumentTI/',
        default='Undefined File',
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
        _('Descrição do arquivo'),
        max_length=255,
        blank=True,
        null=True,
    )

    map_dimension = models.CharField(
        _('Dimensão da página do mapa'),
        max_length=2,
        blank=True,
        null=True,
    )

    js_ti = models.CharField(
        _('Matriz de Terras Indígenas'),
        max_length=255,
        blank=True,
        null=True,
    )

    file = models.FileField(
        _('Caminho do Aqruivo'),
        upload_to='DocsMapoteca/',
        default='Undefined File',
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
