import os
from django.conf import settings
from emails.send_email import send_html_email


def send_email_ticket_to_admins(ticket, data, requesting_email, admin_emails):

    subject = "Nova sugestão analisada"

    main_title = "Nova sugestão analisada"

    body_content = f"""
            <p>
                Prezado(a) administrador(a)/desenvolvedor(a),
                Informamos que uma nova solicitação foi analisada.
                <br />
                O(a) usuário(a) <strong>{requesting_email}</strong> 
                enviou uma crítica ou sugestão identificada pelo código
                <strong>{data['ticket_id']} - {ticket.subject}</strong>,
                passou por avaliação.<br /><br />
                Para mais detalhes e acompanhamento do processo, acesse a
                plataforma.<br /><br />
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

    admin_template = os.path.join(
        settings.EMAIL_TEMPLATES_DIR,
        'default.html'
    )

    send_html_email(
        subject=subject,
        template_path=admin_template,
        context=email_context,
        recipient_list=admin_emails,
    )
