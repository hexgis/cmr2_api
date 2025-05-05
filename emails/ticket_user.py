import os
from django.conf import settings
from emails.send_email import send_html_email


def send_ticket_email_to_user(ticket, data, admin_emails):

    subject = "Sua sugestão foi analisada"

    main_title = "Sua sugestão foi analisada"

    body_content = f"""
            <p>
            Prezado(a) usuário(a), Agradecemos por contribuir com sua sugestão ou
            crítica ao nosso sistema. Informamos que sua solicitação, identificada
            pelo código
            <strong>{data['ticket_id']} - {ticket.subject}</strong>, foi
            devidamente analisada.<br /><br />Você pode acompanhar o processo pela
            plataforma .<br /><br />
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
    }

    template = os.path.join(
        settings.EMAIL_TEMPLATES_DIR,
        'default.html'
    )

    subject = "Sua sugestão foi analisada"

    send_html_email(
        subject=subject,
        template_path=template,
        context=email_context,
        recipient_list=admin_emails,
    )
