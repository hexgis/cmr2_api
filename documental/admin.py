from django.contrib import admin

from documental import models


class ActionAdmin(admin.ModelAdmin):
    list_display = (
    	'no_acao',
	    'dt_cadastro',
	)

    fields = list_display

    search_fields = list_display



class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
    )
    fields = list_display

    search_fields = list_display
    
    
class DocumentosTIAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'path_documento',
        'no_documento',
        'no_extensao',
        'no_ti',
        'usuario_id',
        'st_disponivel',
        'st_excluido',
        'dt_cadastro',
        'dt_atualizacao',
        'co_funai',
        'acao_id',
        'dt_documento',
    )
    
    fields = list_display
    
    search_fields = list_display


class MapasUsoOcupacaoSoloAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'path_documento',
        'no_documento',
        'co_funai',
        'st_disponivel',
        'st_excluido',
        'nu_ano',
        'dt_cadastro',
        'dt_atualizacao',
        'tipo_id',
        'usuario_id',
        'nu_ano_mapa',
    )
    
    fields = list_display
    
    search_fields = list_display

    
class DocumentalDocsAdmin(admin.ModelAdmin):
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
        'acao_id',
        'no_extensao',
        'no_ti',
        'dt_documento',
        'nu_ano',
        'nu_ano_mapa',
    )
    
    fields = list_display
    
    search_fields = list_display


    
admin.site.register(models.Action, ActionAdmin)
admin.site.register(models.Usuario, UsuarioAdmin)
admin.site.register(models.DocumentosTI, DocumentosTIAdmin)
admin.site.register(models.MapasUsoOcupacaoSolo, MapasUsoOcupacaoSoloAdmin)
admin.site.register(models.DocumentalDocs, DocumentalDocsAdmin)
