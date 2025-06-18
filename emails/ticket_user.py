import os
from django.conf import settings
from emails.send_email import send_html_email, get_admin_and_dev_emails


def send_email_ticket_to_user(ticket, data):

    subject = "Sua sugestão foi analisada"

    main_title = "Sua sugestão foi analisada"

    body_content = f"""
            <p>
            Prezado(a) usuário(a)
            , agradecemos por contribuir com sua sugestão ou crítica ao nosso sistema.  
            Informamos que sua solicitação
            , identificada pelo código
            <strong>{data['ticket_id']} - {ticket.subject}</strong>
            , foi analisada.
            <br />
            Para acompanhar detalhes do andamento da demanda, acesse a plataforma.
            <br /><br />
           </p>
        """

    button = f"""
            <a
                href="{settings.RESET_PASSWORD_URL.rstrip('/')}/admin/criticas/{data['ticket_id']}/"
                style="
                background-color: #d92b3f;
                color: #ffffff;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                "
            >
                Acesso ao sistema
            </a>
        """

    email_context = {
        'main_title': main_title,
        'body_content': body_content,
        'ticket_name': ticket.subject,
        'button': button,
        'environment': settings.ENVIRONMENT,
    }

    template = os.path.join(
        settings.EMAIL_TEMPLATES_DIR,
        'default.html'
    )

    subject = "Sua sugestão foi analisada"

    admin_emails = get_admin_and_dev_emails(extra_emails=['cmr@funai.gov.br'])

    send_html_email(
        subject=subject,
        template_path=template,
        context=email_context,
        recipient_list=admin_emails,
    )
