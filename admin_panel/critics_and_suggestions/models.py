from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime
from django.core.exceptions import ValidationError
    
class Ticket(models.Model):
    class SolicitationType(models.IntegerChoices):
        ERRO = 1, 'Erro'
        MELHORIA = 2, 'Melhoria'
        NOVA_FUNCINALIDADE = 3, 'Nova Funcionalidade'
        OUTROS = 4, 'Outros'
    
    class Complexity(models.IntegerChoices):
        FIB_1 = 1, '1'
        FIB_2 = 2, '2'
        FIB_3 = 3, '3'
        FIB_5 = 5, '5'
        FIB_8 = 8, '8'
        FIB_13 = 13, '13'
        FIB_21 = 21, '21'

    code = models.AutoField(
        primary_key=True
        )    
    solicitation_type_code = models.IntegerField(
        choices=SolicitationType.choices,
        default=SolicitationType.ERRO,
    )
    functionality = models.ForeignKey(
        'TicketFunctionality',
        on_delete=models.DO_NOTHING,
        )     
    requesting = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING
        )  
    subject = models.CharField(
        max_length=100,
        null=False,
        blank=False
        )    
    description = models.CharField(
        max_length=100,
        null=False,
        blank=False
        )    
    opened_in = models.DateTimeField(
        auto_now_add=True
        )

    complexity_code = models.IntegerField(
        choices=Complexity.choices,
        default=Complexity.FIB_1
    )
    
    def __str__(self):
        return f"{self.subject} - {self.requesting.username}"
    
    class Meta:
        app_label='admin_panel'
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        db_table = 'admin_panel_tickets'

def rename_file_ticket(instance, filename):
    ticket_id = instance.ticket.code
    ext = filename.split('.')[-1]
    new_filename = f"ticket_{ticket_id}_{datetime.now().strftime('%Y-%m-%d')}.{ext}"
    return os.path.join('attachments/critcs_and_suggestions/question', new_filename)

class TicketAttachment(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        related_name='attachments', 
        on_delete=models.CASCADE
        )
    file = models.FileField(upload_to=rename_file_ticket)

    class Meta:
        app_label='admin_panel'
        verbose_name = "Ticket Attachment"
        verbose_name_plural = "Tickets Attachments"
        db_table = 'admin_panel_tickets_attachment'

class TicketStatus(models.Model):

    class Status(models.IntegerChoices):
        NAO_ANALISADO = 1, 'Não Analisado'
        DEFERIDO = 2, 'Deferido'
        EM_ANALISE = 3, 'Em Análise'
        INDEFERIDO = 4, 'Indeferido'
        EM_DESENVOLVIMENTO = 5, 'Em Desenvolvimento'
        AGUARDANDO_GESTOR = 6, 'Aguardando Gestor'
    
    class Priority(models.IntegerChoices):
        BAIXA = 1, 'Baixa',
        MEDIA = 2, 'Media',
        ALTA = 3, 'Alta',
    
    status_code = models.IntegerField(
        choices=Status.choices,
        default=Status.NAO_ANALISADO,
    )

    priority_code = models.IntegerField(
        choices=Priority.choices,
        default=Priority.BAIXA,
        )
        
    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
    )
    analyzed_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
        )  
    analyzed_in = models.DateTimeField(
        null=True,
        blank=True
        )
    
    class Meta:
        app_label = 'admin_panel'
        verbose_name = "Ticket Status"
        verbose_name_plural = "Tickets Status"
        db_table = 'admin_panel_tickets_status'


    def __str__(self):
        return f"{self.get_status_code_display()} para o Ticket {self.ticket.id}"
    
def rename_file_ticket_status(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"ticket_answer_{instance.ticket_status.ticket.code}_{datetime.now().strftime('%Y-%m-%d')}.{ext}"
    return os.path.join('attachments/critcs_and_suggestions/answer', new_filename)

class TicketStatusAttachment(models.Model):
    ticket_status = models.ForeignKey(
        'TicketStatus', 
        related_name='status_attachments', 
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to=rename_file_ticket_status)

    class Meta:
        app_label = 'admin_panel'
        verbose_name = "Ticket Status Attachment"
        verbose_name_plural = "Tickets Status Attachments"
        db_table = 'admin_panel_tickets_status_attachments'

class TicketFunctionality(models.Model):

    func_name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    

    class Meta:
        app_label = 'admin_panel'
        verbose_name = "Ticket Functionality"
        verbose_name_plural = "Tickets Functionalities"
        db_table = 'admin_panel_tickets_funcionality'

class TicketAnalysisHistory(models.Model):

    analyzed_update = models.DateTimeField(
            auto_now_add=True,
        )
    
    comment = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )

    author = models.ForeignKey(
        User, 
        on_delete=models.DO_NOTHING, 
        )
    
    status_code = models.IntegerField( 
        choices=TicketStatus.Status.choices,  
        null=True,  
        blank=True 
    )

    ticket = models.ForeignKey(
        'Ticket',
        on_delete=models.CASCADE,
    )

    class Meta:
        app_label = 'admin_panel'
        verbose_name = "Ticket Analysis History"
        verbose_name_plural = "Tickets Analysis History"
        db_table = 'admin_panel_tickets_analysis_history'