from django.contrib import admin
from .models import (
    Ticket, TicketAttachment, TicketStatus, TicketStatusAttachment,
    TicketAnalysisHistory, TicketFunctionality
)


class TicketAttachmentInline(admin.TabularInline):
    model = TicketAttachment
    extra = 1


class TicketAnalysisHistoryInline(admin.TabularInline):
    model = TicketAnalysisHistory
    extra = 1


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('code', 'subject', 'solicitation_type',
                    'requesting', 'opened_in', 'complexity_code')
    list_filter = ('solicitation_type', 'complexity_code', 'opened_in')
    search_fields = ('subject', 'description', 'requesting__username')
    inlines = [TicketAttachmentInline, TicketAnalysisHistoryInline]


class TicketStatusAttachmentInline(admin.TabularInline):
    model = TicketStatusAttachment
    extra = 1


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'status_category', 'sub_status',
                    'priority_code', 'analyzed_by', 'analyzed_in', 'due_on')
    list_filter = ('status_category', 'sub_status', 'priority_code')
    search_fields = ('ticket__subject', 'analyzed_by__username')
    inlines = [TicketStatusAttachmentInline]


@admin.register(TicketAnalysisHistory)
class TicketAnalysisHistoryAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'sub_status', 'analyzed_update')
    list_filter = ('sub_status', 'analyzed_update')
    search_fields = ('ticket__subject', 'author__username', 'comment')


@admin.register(TicketFunctionality)
class TicketFunctionalityAdmin(admin.ModelAdmin):
    list_display = ('func_name',)
    search_fields = ('func_name',)


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'name_file')
    search_fields = ('name_file',)
