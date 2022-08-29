from django.contrib import admin

from documental import models


class DocsActionAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsAction` data."""

    list_display = (
    	'id_action',
        'no_action',
        'action_type',
        'description',
	)

    fields = list_display

    search_fields = list_display



class UsuarioAdmin(admin.ModelAdmin):
    """Django administrator `model.Usuario` data."""

    list_display = (
        'id_user',
        'first_name',
    )
    fields = list_display

    search_fields = list_display
 
   
class DocumentalDocsAdmin(admin.ModelAdmin):
    """Django administrator `model.DocumentalDocs` data."""

    list_display = (
        'id_document',
        'path_document',
        'no_document', 
        'usercmr_id',
        'st_available',
        'st_excluded',
        'dt_registration',
        'dt_update',
        'co_funai',
        'action_id',
        'no_extension',
        'no_ti',
        'co_cr',
        'ds_cr',
        'dt_document',
        'nu_year',
        'nu_year_map',
    )
    
    fields = list_display
    
    search_fields = list_display


admin.site.register(models.DocsAction, DocsActionAdmin)
admin.site.register(models.UsersCMR, UsuarioAdmin)
admin.site.register(models.DocumentalDocs, DocumentalDocsAdmin)
