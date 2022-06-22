from django.db import models
from django.utils.translation import ugettext_lazy as _

from documental.utils import (
    diretorio_mapas_uso_solo,
    diretorio_ti
)


class Action(models.Model):
    """Action model data for documental model."""

    # id = models.IntegerField(
    #     _('Primary key'),
    #     unique=True,
    #     primary_key=True,
    # )

    no_acao = models.CharField(
        _('Action name'),
        max_length=255,
        unique=True,
    )

    dt_cadastro = models.DateTimeField(
        _('Registration date'),
        null=True,
        blank=True,
    )
    class Meta:
        """"Meta class for `documental.Action` model."""
        app_label = 'documental'
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'

    
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


class DocumentosTI(models.Model):
    """DocumentosTI model data for documental model."""

    id = models.IntegerField(
        _('Primary key'),
        unique=True,
        primary_key=True,
    )
    
    # path_documento = models.FileField(
	# 	_('Document path'),
	# 	upload_to=diretorio_ti,
    #     max_length=255,
	# )

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

    no_extensao = models.CharField(
    	_('Document extension'),
    	max_length=255,
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
    	_('Funai code - Indigenou Lands'),
        null=True,
        blank=True,
    )

    no_ti = models.CharField(
    	_('Indigenou Lands name'),
    	max_length=255,
        null=True,
        blank=True,
    )

    acao_id = models.ForeignKey(
    	'documental.Action',
        on_delete=models.DO_NOTHING,
        related_name='documentosti_type',
    	# blank=False,
    	null=False,
    )
    
    usuario_id = models.ForeignKey(
    	'documental.Usuario',
        on_delete=models.DO_NOTHING,
        related_name='documentosti_usuario_id',
        # blank=False,
    	null=False,
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

    dt_documento = models.DateField(
    	_('Date of document'),
    	null=True,
    	blank=True,
    )

    class Meta:
        """"Meta class for `documental.DocumentosTI` model."""
        app_label = 'documental'
        verbose_name = 'DocumentTI'
        verbose_name_plural = 'DocumentsTI'
        # db_table = 'painel\".\"manager_documentosti'
        # managed = False


class MapasUsoOcupacaoSolo(models.Model):
    """MapasUsoOcupacaoSolo model data for documental model."""

    id = models.IntegerField(
        _('Primary key'),
        unique=True,
        primary_key=True,
    )
    
    # path_documento = models.FileField(
	# 	_('Document path'),
	# 	upload_to=diretorio_mapas_uso_solo,
    #     max_length=255,
	# )

    path_documento = models.CharField(
		_('Document path'),
        max_length=255,
        null=True,
        blank=True,
	)

    no_documento = models.CharField(
    	_('Document name'),
    	max_length=555,
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
    	_('Funai code - Indigenou Lands'),
        null=True,
        blank=True,
    )

    tipo_id = models.ForeignKey(
        'documental.Action',
        on_delete=models.DO_NOTHING,
        related_name='Maps_type',
    	# blank=False,
    	null=False,
    )
    
    usuario_id = models.ForeignKey(
    	'documental.Usuario',
        on_delete=models.DO_NOTHING,
        related_name='Maps_usuario_id',
        # blank=False,
    	null=False,
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
        # auto_now_add=true, ???
        null=True,
        blank=True,
    )

    dt_atualizacao = models.DateTimeField(
    	_('Last update date'),
        # auto_now=true, ???
        null=True,
        blank=True,
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
        """"Meta class for `documental.MapasUsoOcupacaoSolo` model."""
        app_label = 'documental'
        verbose_name = 'Use Land Occupancy Map'
        verbose_name_plural = 'Use Land Occupancy Maps'
        # db_table = 'painel\".\"manager_mapasusoocupacaosolo'
        # managed = False

























class DocumentalDocs(models.Model):
    """DocumentalDocs model data for documental model."""

    id = models.IntegerField(
        _('Primary key'),
        unique=True,
        primary_key=True,
    )
    
    # path_documento = models.FileField(
	# 	_('Document path'),
    #     # adicionar condição para saber de qual ditretória irá ser realizado 
    #     # o acesso aos mapas: "diretorio_mapas_uso_solo" ou "diretorio_ti"
	# 	upload_to=diretorio_ti,
    #     max_length=255,
	# )

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
        # blank=False,
    	null=False,
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

    acao_id = models.ForeignKey(
    	'documental.Action',
        on_delete=models.DO_NOTHING,
        related_name='documentosdocs_type',
    	# blank=False,
    	null=False,
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
        return self.path_documento
