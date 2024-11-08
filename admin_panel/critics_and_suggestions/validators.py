from django.core.exceptions import ValidationError
from .models import Ticket, TicketStatus

def validate_status_ticket_choices(ticket_status):
    errors = {}

    if ticket_status.status_code not in dict(TicketStatus.Status.choices):
            errors['status_code'] = 'Invalid status.'
    
    if ticket_status.priority_code not in dict(TicketStatus.Priority.choices):
            errors['priority_code'] = 'Invalid priority.'

    if errors:
        raise ValidationError(errors)

def validate_ticket_choices(ticket):
    errors = {}

    if ticket.solicitation_type not in dict(Ticket.SolicitationType.choices):
        errors['solicitation_type'] = 'Invalid solicitation type.'

    if errors:
        raise ValidationError(errors)