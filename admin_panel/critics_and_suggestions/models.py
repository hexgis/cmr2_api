from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime
from django.utils.translation import gettext_lazy as _

class Ticket(models.Model):
    class SolicitationType(models.TextChoices):
        ERRO = "ERRO", "Erro"
        MELHORIA = "MELHORIA", "Melhoria"
        NOVA_FUNCINALIDADE = "NOVA_FUNCIONALIDADE", "Nova Funcionalidade"
        OUTROS = "OUTROS", "Outros"
    
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
        
    solicitation_type = models.CharField(
        max_length=20,
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
    
    class StatusCategory(models.TextChoices):
        NAO_ANALISADO = "NAO_ANALISADO", "Não Analisado"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em Andamento"
        CONCLUIDO = "CONCLUIDO", "Concluído"
        RECUSADO = "RECUSADO", "Recusado"

    class SubStatus(models.TextChoices):
        # Substatus para 'Em Andamento'
        AGUARDANDO_GESTOR = "AGUARDANDO_GESTOR", "Aguardando Gestor"
        EM_DESENVOLVIMENTO = "EM_DESENVOLVIMENTO", "Em Desenvolvimento"
        
        # Substatus para 'Concluído'
        CONCLUIDO = "CONCLUIDO", "Concluído"
        EM_TESTE = "EM_TESTE", "Em Teste"
        
        # Substatus para 'Recusado'
        INVIAVEL = "INVIAVEL", "Inviável"
        INDEFERIDO = "INDEFERIDO", "Indeferido"
    
    class Priority(models.IntegerChoices):
        BAIXA = 1, 'Baixa',
        MEDIA = 2, 'Media',
        ALTA = 3, 'Alta',
    
    status_category = models.CharField(
        max_length=20,
        choices=StatusCategory.choices,
        default=StatusCategory.NAO_ANALISADO,
    )
    
    sub_status = models.CharField(
        max_length=20,
        choices=SubStatus.choices,
        null=True,
        blank=True
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
    
    due_on = models.DateField(
        null=True,
        blank=True
    )
    
    class Meta:
        app_label = 'admin_panel'
        verbose_name = "Ticket Status"
        verbose_name_plural = "Tickets Status"
        db_table = 'admin_panel_tickets_status'


    def __str__(self):
        return f"{self.get_status_category_display()} para o Ticket {self.ticket.id}"
    
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
    
    sub_status = models.CharField(
        max_length=20,
        choices= TicketStatus.SubStatus.choices,
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
