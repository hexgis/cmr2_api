from django.db import models
from django.utils.translation import ugettext_lazy as _

from documentary.utils import (
    diretorio_mapas_uso_solo,
    diretorio_ti
)


class Acao(models.Model):
    """Acao model data for documentary model."""
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
        """"Meta class for `documentary.Acao` model."""
        app_label = 'documentary'
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'


class Usuario(models.Model):
    """Usuario model data for documentary model."""
    id = models.IntegerField(
        _('User id key'),
        unique=True,
        primary_key=True,
    )

    first_name = models.CharField(
        _('Name of who registered'),
        max_length=255,
        unique=True,
    )
    
    class Meta:
        """"Meta class for `documentary.Usuario` model."""
        app_label = 'documentary'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        # db_table = 'painel\".\"auth_user'
        # managed = False


class DocumentosTI(models.Model):
    """DocumentosTI model data for documentary model."""
    id = models.IntegerField(
        _('Primary key'),
        unique=True,
        primary_key=True,
    )
    
    path_documento = models.FileField(
		_('Document path'),
		upload_to=diretorio_ti,
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

    acao = models.ForeignKey(
    	'documentary.Acao',
        on_delete=models.DO_NOTHING,
        related_name='documentosti_type',
    	# blank=False,
    	null=False,
    )
    
    usuario_id = models.ForeignKey(
    	'documentary.Usuario',
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
        """"Meta class for `documentary.DocumentosTI` model."""
        app_label = 'documentary'
        verbose_name = 'DocumentTI'
        verbose_name_plural = 'DocumentsTI'
        # db_table = 'painel\".\"manager_documentosti'
        # managed = False


class MapasUsoOcupacaoSolo(models.Model):
    """MapasUsoOcupacaoSolo model data for documentary model."""
    id = models.IntegerField(
        _('Primary key'),
        unique=True,
        primary_key=True,
    )
    
    path_documento = models.FileField(
		_('Document path'),
		upload_to=diretorio_ti,
	)

    no_documento = models.CharField(
    	_('Document name'),
    	max_length=255,
        null=True,
        blank=True,
    )

    co_funai = models.IntegerField(
    	_('Funai code - Indigenou Lands'),
        null=True,
        blank=True,
    )

    tipo_id = models.ForeignKey(
    	'documentary.Acao',
        on_delete=models.DO_NOTHING,
        related_name='Maps_type',
    	# blank=False,
    	null=False,
    )
    
    usuario_id = models.ForeignKey(
    	'documentary.Usuario',
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
        """"Meta class for `documentary.MapasUsoOcupacaoSolo` model."""
        app_label = 'documentary'
        verbose_name = 'Use Land Occupancy Map'
        verbose_name_plural = 'Use Land Occupancy Maps'
        # db_table = 'painel\".\"manager_mapasusoocupacaosolo'
        # managed = False

























class DocumentaryDocs(models.Model):
    """DocumentaryDocs model data for documentary model."""
    id = models.IntegerField(
        _('Primary key'),
        unique=True,
        primary_key=True,
    )
    
    path_documento = models.FileField(
		_('Document path'),
		upload_to=diretorio_ti,
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

    acao = models.ForeignKey(
    	'documentary.Acao',
        on_delete=models.DO_NOTHING,
        related_name='documentosdocs_type',
    	# blank=False,
    	null=False,
    )
    
    usuario_id = models.ForeignKey(
    	'documentary.Usuario',
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
        """"Meta class for `documentary.DocumentosTI` model."""
        app_label = 'documentary'
        verbose_name = 'Documentary Doc'
        verbose_name_plural = 'Documentary Docs'
