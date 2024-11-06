from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from admin_panel.critics_and_suggestions.models import TicketStatus
from datetime import date
import os

emails_dev_list = ['valdean.junior@hex360.com.br', 'marcos.silva@hex360.com.br']

def get_expiration_date():
    tickets = TicketStatus.objects.all()
    dates_dict = {}
    
    for ticket in tickets:
        ticket_id = ticket.ticket
        ticket_name = ticket_id.subject
        due_on = ticket.due_on
        description = ticket_id.description
        category = ticket.status_category

        days_to_expire = (due_on - date.today()).days
        dates_dict[ticket_id.code] = {'due_on': due_on, 'days_to_expire': days_to_expire, 'ticket_name': ticket_name, 'description': description, 'category': category}
    
    send_ticket_email(dates_dict)

def send_ticket_email(dates_dict):
    #'NAO_ANALISADO', 'EM_ANDAMENTO'
    for ticket_id, details in dates_dict.items():
        ticket_name = details['ticket_name']
        days_to_expire = details['days_to_expire']
        expire_date = details['due_on']
        description = details['description']
        category = details['category']
        
        if category in ['NÃO_ANALISADO', 'EM_ANDAMENTO'] and days_to_expire <= 3:
            template_path = os.path.join(settings.MEDIA_ROOT, 'templates/emails', 'ticket_expiration.html')
                        
            html_content = render_to_string(template_path, {
                'ticket_name': ticket_name,
                'due_on': days_to_expire,
                'link': f"http://localhost:8080/adm-panel/tickets/status-update/{ticket_id}/",
                'expire_date': expire_date,
                'desciption': description
            })
            # 🦆 alterar para o link do CMR para funcionar
            text_content = strip_tags(html_content) 
            
            email = EmailMultiAlternatives(
                subject="Status da Solicitação de Acesso",
                body=text_content,
                from_email="hexgisdev@gmail.com",
                to=['marcos.silva@hex360.com.br', 'valdean.junior@hex360.com.br', 'joao.fonseca@hex360.com.br']
            )
            
            # Anexa o conteúdo HTML
            email.attach_alternative(html_content, "text/html")
            
            email.send()
            print(f"Email enviado para o ticket '{ticket_name}' com {days_to_expire} dias restantes.")