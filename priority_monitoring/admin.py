from django.contrib import admin

from priority_monitoring import models


class PriorityConsolidatedTempAdmin(admin.ModelAdmin):
    list_display = (
        'no_estagio',
        'no_cr',
        'no_ti',
        'ranking',
        'prioridade',
        'flag',
        'dt_t_um',
    )
    fields = list_display
    search_fields = (
        'no_cr',
        'no_ti',
        'dt_t_um',
        #'start_date',
        #'end_date',
        'ranking',
    )
    list_filter = (
        'no_cr',
        'no_ti',
        #'start_date',
        #'end_date',
        'ranking',
    )
class PriorityConsolidatedAdmin(admin.ModelAdmin):
    list_display = (
        'id_tb',
        'tb_ciclo_monitoramento_id',
        'no_estagio',
        'no_image',
        'dt_image',
        'nu_orbita',
        'nu_ponto',
        'dt_t0',
        'dt_t1',
        'nu_area_km2',
        'nu_area_ha',
        'nu_latitude',
        'nu_longitude',
        'tempo',
        'contribuicao',
        'velocidade',
        'contiguidade',
        'ranking',
        'prioridade',
        'dt_cadastro',
        'geom',
    )
    fields = list_display

admin.site.register(models.PriorityConsolidated, PriorityConsolidatedAdmin)
admin.site.register(models.PriorityConsolidatedTemp, PriorityConsolidatedTempAdmin)