from django.db import models
from django.contrib.auth import get_user_model
import os
from datetime import datetime
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
        null=True,
        blank=True,
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
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Description of the ticket",
        null=False,
        blank=False
    )
    opened_in = models.DateTimeField(
        auto_now_add=True
    )

    complexity_code = models.IntegerField(
        choices=Complexity.choices,
        default=Complexity.FIB_1,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.subject} - {self.requesting.username}"

    class Meta:
        app_label = 'admin_panel'
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
    file_path = models.FileField(
        upload_to=rename_file_ticket
    )
    name_file = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    class Meta:
        app_label = 'admin_panel'
        verbose_name = "Ticket Attachment"
        verbose_name_plural = "Tickets Attachments"
        db_table = 'admin_panel_tickets_attachment'

    def save(self, *args, **kwargs):
        if self.file_path and not self.name_file:
            self.name_file = os.path.basename(self.file_path.name)
        super().save(*args, **kwargs)


class TicketStatus(models.Model):

    class StatusCategory(models.TextChoices):
        NAO_ANALISADO = "NAO_ANALISADO", "Não Analisado"
        EM_ANDAMENTO = "EM_ANDAMENTO", "Em Andamento"
        CONCLUIDO = "CONCLUIDO", "Concluído"
        RECUSADO = "RECUSADO", "Recusado"
        DEFERIDO = "DEFERIDO", "Deferido"
        DESENVOLVIDO = "DESENVOLVIDO", "Desenvolvido"



    class Priority(models.TextChoices):
        BAIXA = 'BAIXA', 'Baixa',
        MEDIA = 'MEDIA', 'Média',
        ALTA = 'ALTA', 'Alta',

    status_category = models.CharField(
        max_length=20,
        choices=StatusCategory.choices,
        default=StatusCategory.NAO_ANALISADO,
        null=True,
        blank=True
    )

    priority_code = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.BAIXA,
        null=True,
        blank=True
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
        return f"{self.get_status_category_display()} para o Ticket {self.ticket.code}"


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
    ticket_history = models.ForeignKey(
        'TicketAnalysisHistory',
        related_name='status_history_attachments',
        on_delete=models.CASCADE
    )
    file_path = models.FileField(
        upload_to=rename_file_ticket_status
    )
    name_file = models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    class Meta:
        app_label = 'admin_panel'
        verbose_name = "Ticket Status Attachment"
        verbose_name_plural = "Tickets Status Attachments"
        db_table = 'admin_panel_tickets_status_attachments'

    def save(self, *args, **kwargs):
        if self.file_path and not self.name_file:
            self.name_file = os.path.basename(self.file_path.name)
        super().save(*args, **kwargs)


class TicketAnalysisHistory(models.Model):

    analyzed_update = models.DateTimeField(
        auto_now_add=True,
    )

    comment = models.TextField(
        verbose_name="Comentário",
        help_text="Comment about the ticket analysis",
        blank=False,
        null=False
    )

    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
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
