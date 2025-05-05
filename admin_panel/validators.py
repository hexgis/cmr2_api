from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Ticket, TicketStatus
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime

from rest_framework.exceptions import ValidationError
from datetime import datetime, date


def validate_ticket_choices(ticket):
    """
    Validates the ticket's solicitation type against the allowed choices.

    Args:
        ticket (Ticket): The ticket instance to validate.

    Raises:
        ValidationError: If the solicitation type is invalid.
    """
    errors = {}

    if ticket.solicitation_type not in dict(Ticket.SolicitationType.choices):
        errors['solicitation_type'] = 'Invalid solicitation type.'

    if errors:
        raise ValidationError(errors)


def validate_status_and_substatus(status_category, sub_status, current_status=None, current_substatus=None):
    """
    Validates the compatibility between the status category and substatus.

    Args:
        status_category (str): The received status category.
        sub_status (str): The received substatus.
        current_status (str, optional): The current status of the ticket. Default is None.
        current_substatus (str, optional): The current substatus of the ticket. Default is None.

    Raises:
        ValidationError: If the combination of status category and substatus is invalid.
    """
    # Ensure no transition to "Não Analisado" unless the current status is "Recusado"
    if current_status == TicketStatus.StatusCategory.RECUSADO and current_substatus in (
        TicketStatus.SubStatus.INDEFERIDO,
        TicketStatus.SubStatus.INVIAVEL,
    ):
        if status_category != TicketStatus.StatusCategory.NAO_ANALISADO or sub_status != TicketStatus.SubStatus.NAO_ANALISADO:
            raise ValidationError(
                "Transição não permitida! O status 'RECUSADO' com substatus 'INDEFERIDO' ou 'INVIAVEL' só pode ser alterado para 'NAO_ANALISADO'.")

    # Ensure "Deferido" status is only valid from "Não Analisado"
    if current_status and current_status != TicketStatus.StatusCategory.NAO_ANALISADO:
        if status_category == TicketStatus.StatusCategory.DEFERIDO:
            raise ValidationError(
                "Não é permitido alterar o status para 'Deferido'.")

    # Validate valid substatus for each status category
    valid_substatus = {
        TicketStatus.StatusCategory.DEFERIDO: [
            TicketStatus.SubStatus.DEFERIDO
        ],
        TicketStatus.StatusCategory.RECUSADO: [
            TicketStatus.SubStatus.INVIAVEL,
            TicketStatus.SubStatus.INDEFERIDO,
        ],
        TicketStatus.StatusCategory.EM_ANDAMENTO: [
            TicketStatus.SubStatus.AGUARDANDO_GESTOR,
            TicketStatus.SubStatus.EM_DESENVOLVIMENTO,
        ],
        TicketStatus.StatusCategory.CONCLUIDO: [
            TicketStatus.SubStatus.CONCLUIDO,
            TicketStatus.SubStatus.EM_TESTE,
            TicketStatus.SubStatus.DESENVOLVIDO,
        ],
    }

    if status_category in valid_substatus:
        if sub_status not in valid_substatus[status_category]:
            raise ValidationError(
                f"O substatus '{sub_status}' não é válido para a categoria '{status_category}'."
            )


def validate_complexity(complexity_code):
    """
    Validates the ticket's complexity code against the allowed choices.

    Args:
        complexity_code (str): The complexity code to validate.

    Raises:
        ValidationError: If the complexity code is invalid.
    """
    if complexity_code not in [choice[0] for choice in Ticket.Complexity.choices]:
        raise ValidationError(
            f"O código de complexidade '{complexity_code}' é inválido. Escolhas válidas: {', '.join([str(choice[0]) for choice in Ticket.Complexity.choices])}")


def format_datetime(datetime_obj, fmt='%d/%m/%Y %H:%M:%S'):
    """
    Formats a datetime object into a string based on the provided format.

    Args:
        datetime_obj (datetime): The datetime object to format.
        fmt (str, optional): The format string. Default is '%d/%m/%Y %H:%M:%S'.

    Returns:
        str: The formatted datetime string, or None if the datetime object is None.
    """
    return localtime(datetime_obj).strftime(fmt) if datetime_obj else None


def format_date(date_obj, fmt='%d/%m/%Y'):
    """
    Formats a date object into a string based on the provided format.

    Args:
        date_obj (date): The date object to format.
        fmt (str, optional): The format string. Default is '%d/%m/%Y'.

    Returns:
        str: The formatted date string, or None if the date object is invalid.
    """
    return date_obj.strftime(fmt) if isinstance(date_obj, date) else None
