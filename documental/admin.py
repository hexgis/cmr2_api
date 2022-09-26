from django.contrib import admin

from documental import models


list_documental_abstract_class = [
    'id_document',
    'path_document',
    'no_document',
    'usercmr_id',
    'st_available',
    'st_excluded',
    'dt_registration',
    'dt_update',
    'co_funai',
    'no_ti',
    'co_cr',
    'ds_cr',
    'action_id',
]


class DocsActionAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsAction` data."""

    list_display = (
        'id_action',
        'no_action',
        'dt_creation',
        'action_type',
        'action_type_group',
        'description',
    )

    fields = list_display

    search_fields = list_display


class UsersCMRAdmin(admin.ModelAdmin):
    """Django administrator `model.Usuario` data."""

    list_display = (
        'id_user',
        'first_name',
    )

    fields = list_display

    search_fields = list_display


class DocsDocumentTIAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsDocumentTI` data."""

    list_display = [
        'no_extension',
        'dt_document',
    ] + list_documental_abstract_class

    fields = list_display

    search_fields = list_display


class DocsLandUserAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsLandUser` data."""

    list_display = [
        'nu_year',
        'nu_year_map',
    ] + list_documental_abstract_class

    fields = list_display

    search_fields = list_display


class DocsMapotecaAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsMapoteca` data."""

    list_display = [
        'no_description',
        'map_dimension',
        'js_ti',
    ] + list_documental_abstract_class

    fields = list_display

    search_fields = list_display


class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = [
        # 'uploaded_at',
        'file',
        'dt_cadastro',
        'id_acao'
    ]

    fields = list_display

    search_fields = list_display


admin.site.register(models.DocsAction, DocsActionAdmin)
admin.site.register(models.UsersCMR, UsersCMRAdmin)
admin.site.register(models.DocsDocumentTI, DocsDocumentTIAdmin)
admin.site.register(models.DocsLandUser, DocsLandUserAdmin)
admin.site.register(models.DocsMapoteca, DocsMapotecaAdmin)

admin.site.register(models.DocumentUpload, DocumentUploadAdmin)
