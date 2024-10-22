from django.contrib import admin
from .critics_and_suggestions.models import TicketFunctionality 

@admin.register(TicketFunctionality)
class TicketFunctionalityAdmin(admin.ModelAdmin):
    list_display = ('id', 'func_name')
    search_fields = ('func_name',)
