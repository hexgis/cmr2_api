from django.core.exceptions import ValidationError
from .models import Ticket
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from datetime import datetime

def validate_ticket_choices(ticket):
    errors = {}

    if ticket.solicitation_type not in dict(Ticket.SolicitationType.choices):
        errors['solicitation_type'] = 'Invalid solicitation type.'

    if errors:
        raise ValidationError(errors)

def validate_due_on(value):
    if isinstance(value, list) and len(value) > 0:
        value = value[0]

    if value:
        try:
            due_on = datetime.strptime(value, "%d/%m/%Y").date()
            return due_on
        except ValueError:
            raise ValidationError("Data 'due_on' está no formato errado. Use o formato dd/mm/yyyy.")
    return value