from django.contrib import admin

from .models import(
    PriorityConsolidated,
    PriorityConsolidatedTb
)
from .filters import(
    PriorityConsolidatedFilter
)

class PriorityConsolidatedAdmin(admin.ModelAdmin):
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
class PriorityConsolidatedTbAdmin(admin.ModelAdmin):
    list_display = (
        'tb_ciclo_monitoramento_id',
    	'no_estagio',
	    'no_imagem',
        'dt_imagem',
        'nu_orbita',
        'nu_ponto',
        'dt_t_zero',
        'dt_t_um',
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
        # 'geom',

    )
    fields = list_display

admin.site.register(PriorityConsolidated, PriorityConsolidatedAdmin)
admin.site.register(PriorityConsolidatedTb, PriorityConsolidatedTbAdmin)