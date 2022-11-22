from django.contrib import admin

from documental import models

"""List of common fields for DjangoAdmin classes."""
list_fields_admin_commun = [
    'file',
    'id_document',
    'path_document',
    'no_document',
    'usercmr_id',
    'st_available',
    'st_excluded',
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
        'dt_registration',
    ] + list_fields_admin_commun

    fields = list_fields_admin_commun

    search_fields = list_fields_admin_commun


class DocsLandUserAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsLandUser` data."""

    list_display = [
        'nu_year',
        'nu_year_map',
        'dt_registration',
    ] + list_fields_admin_commun

    fields = list_fields_admin_commun

    search_fields = list_fields_admin_commun


class DocsMapotecaAdmin(admin.ModelAdmin):
    """Django administrator `model.DocsMapoteca` data."""

    list_display = [
        'no_description',
        'map_dimension',
        'js_ti',
        'dt_registration',
    ] + list_fields_admin_commun

    fields = list_fields_admin_commun

    search_fields = list_fields_admin_commun


admin.site.register(models.DocsAction, DocsActionAdmin)
admin.site.register(models.UsersCMR, UsersCMRAdmin)
admin.site.register(models.DocsDocumentTI, DocsDocumentTIAdmin)
admin.site.register(models.DocsLandUser, DocsLandUserAdmin)
admin.site.register(models.DocsMapoteca, DocsMapotecaAdmin)
