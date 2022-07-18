from django.contrib import admin

from documental import models


class DocsActionAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsAction` data."""

    list_display = (
    	'no_acao',
	    'dt_criacao',
        'descricao',
	)

    fields = list_display

    search_fields = list_display



class UsuarioAdmin(admin.ModelAdmin):
    """Django administrator `model.Usuario` data."""

    list_display = (
        'id',
        'first_name',
    )
    fields = list_display

    search_fields = list_display
 
   
class DocumentalDocsAdmin(admin.ModelAdmin):
    """Django administrator `model.DocumentalDocs` data."""

    list_display = (
        'id',
        'path_documento',
        'no_documento',
        'usuario_id',
        'st_disponivel',
        'st_excluido',
        'dt_cadastro',
        'dt_atualizacao',
        'co_funai',
        'id_acao',
        'no_extensao',
        'no_ti',
        'co_cr',
        'ds_cr',
        'dt_documento',
        'nu_ano',
        'nu_ano_mapa',
    )
    
    fields = list_display
    
    search_fields = list_display


admin.site.register(models.DocsAction, DocsActionAdmin)
admin.site.register(models.Usuario, UsuarioAdmin)
admin.site.register(models.DocumentalDocs, DocumentalDocsAdmin)
