import os
from django.conf import settings
from emails.send_email import send_html_email, get_admin_and_dev_emails


def send_email_ticket_to_admins(ticket):

    subject = "Nova sugestão analisada"

    main_title = "Nova sugestão analisada"

    body_content = f"""
            <p>
                Prezado(a) administrador(a) / Desenvolvedor(a)
                , informamos que o chamado identificado pelo código
                <strong>{ticket.code} - {ticket.subject}</strong> 
                , enviado pelo(a) usuário(a) 
                <strong>{ticket.requesting.email}</strong>
                , foi atualizado pela equipe do CMR.
                <br />
                Para mais detalhes e acompanhamento do processo, acesse a
                plataforma.<br /><br />
           </p>
        """

    button = f"""
            <a
                href="{settings.RESET_PASSWORD_URL.rstrip('/')}/admin/criticas/{ticket.code}/"
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

    admin_template = os.path.join(
        settings.EMAIL_TEMPLATES_DIR,
        'default.html'
    )

    admin_emails = get_admin_and_dev_emails(extra_emails=['cmr@funai.gov.br'])

    send_html_email(
        subject=subject,
        template_path=admin_template,
        context=email_context,
        recipient_list=admin_emails,
    )
