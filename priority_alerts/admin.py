from django.contrib import admin

from priority_alerts import models


class PriorityAlertsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'no_ciclo',
        'no_titulo',
        'no_arquivo',
        'nu_referencia',
        'nu_mapa',
        'no_estagio',
        'no_imagem',
        'nu_orbita_ponto',
        'dt_t_zero',
        'dt_t_um',
        'nu_area_ha',
        'co_funai',
        'no_ti',
        'co_cr',
        'ds_cr',
        'no_municipio',
        'sg_uf',
        'nu_longitude',
        'nu_latitude',
    )

    search_fields = (
        (
            'id',
            'no_ciclo',
            'no_titulo',
            'no_arquivo',
            'nu_referencia',
            'nu_mapa',
            'no_estagio',
            'no_imagem',
            'nu_orbita_ponto',
            'co_funai',
            'no_ti',
            'co_cr',
            'ds_cr',
            'sg_uf',
        )
    )
    list_filter = (
        'no_ciclo',
        'no_titulo',
        'sg_uf',
        'no_imagem',
        'nu_orbita_ponto',
        'no_ti',
        'ds_cr',
    )


admin.site.register(models.UrgentAlerts, PriorityAlertsAdmin)
