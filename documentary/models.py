from django.db import models
from django.utils.translation import ugettext_lazy as _



class Acao(models.Model):
    """Acao model data for documentary model."""
    id = models.IntegerField(
        _('primary key'),
        unique=True,
        primary_key=True,
    )

    no_acao = models.CharField(
        _("nome da ação"),
        max_length=255,
        unique=True,
    )

    dt_cadastro = models.DateTimeField(
        _("Data do cadastro"),
        null=True,
        blank=True,
    )
    class Meta:
        """"""
        app_label = 'documentary'
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'
        db_table = 'painel\".\"manager_acao'
        managed = False


class Usuario(models.Model):

    usuario_id = models.IntegerField(
        _('primary key'),
        unique=True,
        primary_key=True,
    )

    first_name = models.CharField(
        _('nome de quem cadastrou'),
        max_length=255,
        unique=True,
    )
    
    class Meta:
        """"""
        app_label = 'documentary'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        # db_table = 'painel\".\"auth_user'
        # managed = False


class DocumentosTI(models.Model):
    """DocumentosTI model data for documentary model."""
    path_documento = models.FileField(
		_("Path do documento"),
		upload_to=self.diretorio_ti()
	)

    no_documento = models.CharField(
    	_("Nome do documento"),
    	max_length=255
    )

    no_extensao = models.CharField(
    	_("Extensão do documento"),
    	max_length=5
    )

    co_funai = models.IntegerField(
    	_("Código da Terra Indígena")
    )

    no_ti = models.CharField(
    	_("Nome da Terra Indígena"),
    	max_length=255
    )

    acao = models.ForeignKey(
    	Acao,
        related_name=_('documentos_ti'),
    	blank=False,
    	null=False,
    )
    
    usuario = models.ForeignKey(
    	Usuario, 
        related_name=_('usuario_id'),
        blank=False,
    	null=False,
    )

    st_disponivel = models.BooleanField(
    	_("Documento disponível"),
    	default=False,
    )

    st_excluido = models.BooleanField(
    	_("Documento excluído"),
    	default=False,
    )

    dt_cadastro = models.DateTimeField(
    	_("Data do cadastro")
    )

    dt_atualizacao = models.DateTimeField(
    	_("Data da ultima atualização")
    )

    dt_documento = models.DateField(
    	_("Data do documento"),
    	null=True,
    	blank=True,
    )
    class Meta:
        """"""
        app_label = 'documentary'
        verbose_name = 'DocumentTI'
        verbose_name_plural = 'DocumentsTI'
        db_table = 'painel\".\"manager_documentosti'
        managed = False

    def diretorio_ti(instance, filename):
        return "documentos_terra_indigena/{0}/{1}".format(instance.no_ti, filename)


# class MapasUsoOcupacaoSolo(models.Model):

#     class Meta:
        # db_table = 'painel\".\"manager_mapasusoocupacaosolo'
        # managed = False


# class DocumentaryDocs(models.Model):

#     class Meta:
