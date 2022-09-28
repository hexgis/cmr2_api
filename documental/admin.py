from django.contrib import admin

from documental import models


class ListDocumentalAbstractClass(admin.ModelAdmin):
    list_displayy = [
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


class DocsDocumentTIAdmin(ListDocumentalAbstractClass):
    """Django administrator `model.DocsDocumentTI` data."""

    list_display = self.list_displayy([
        'no_extension',
        'dt_document',
    ])

    fields = list_display

    search_fields = list_display


class DocsLandUserAdmin(ListDocumentalAbstractClass):
    """Django administrator `model.DocsLandUser` data."""

    list_display = self.list_display.extend([
        'nu_year',
        'nu_year_map',
    ])

    fields = list_display

    search_fields = list_display


class DocsMapotecaAdmin(LucasListDocumentalAbstractClassClass):
    """Django administrator `model.DocsMapoteca` data."""

    list_display = self.list_display.extend([
        'no_description',
        'map_dimension',
        'js_ti',
    ])

    fields = list_display

    search_fields = list_display


admin.site.register(models.DocsAction, DocsActionAdmin)
admin.site.register(models.UsersCMR, UsersCMRAdmin)
admin.site.register(models.DocsDocumentTI, DocsDocumentTIAdmin)
admin.site.register(models.DocsLandUser, DocsLandUserAdmin)
admin.site.register(models.DocsMapoteca, DocsMapotecaAdmin)
