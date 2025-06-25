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
