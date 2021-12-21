from django.contrib import admin

from .models import(
    PriorityConsolidated
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

admin.site.register(PriorityConsolidated, PriorityConsolidatedAdmin)