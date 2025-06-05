import os
from django.conf import settings
from emails.send_email import send_html_email


def send_email_access_request(access_request):

    subject = "Usuário pendente de aprovação"

    main_title = "Usuário pendente de aprovação"

    body_content = f"""
        <p><strong>Prezados(as) Gestores(as)</strong>,</p>
        <p>
          Um novo usuário,<strong> {access_request.name} </strong>, solicitou acesso ao
          Centro de Monitoramento Remoto da Funai. Por questões de segurança, o
          acesso às informações restritas da plataforma só é possível com
          anuência da chefia imediata do servidor interessado.
        </p>
        <p>
          Caso deseje aprovar o acesso de <strong> {access_request.name}</strong>, 
          clique no botão abaixo:
        </p>
        """

    button = f"""
           <a
                href="{settings.RESET_PASSWORD_URL.rstrip('/')}/admin/analisar-solicitacao-acesso/{access_request.id}"
                style="
                background-color: #d92b3f;
                color: #ffffff;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 5px;
                "
            >
                Analisar solicitação de acesso
            </a>
        """

    email_context = {
        'main_title': main_title,
        'body_content': body_content,
        'button': button,
        'environment': settings.ENVIRONMENT,
    }

    template = os.path.join(
        settings.EMAIL_TEMPLATES_DIR,
        'default.html'
    )

    from_email = settings.DEFAULT_FROM_EMAIL

    send_html_email(
        subject=subject,
        template_path=template,
        from_email=from_email,
        context=email_context,
        recipient_list=[access_request.coordinator_email],
    )
