import os
from django.conf import settings
from emails.send_email import send_html_email


def send_email_password(reset_code,  email):

    subject = "Solicitação de Recuperação de Senha do CMR"

    main_title = "Alteração de senha"

    body_content = f"""
            <p>
                Prezado(a) usuário(a), Recebemos uma solicitação para alterar a sua senha. 
                Para completar o processo, por favor, clique no botão abaixo, 
                este link é válido por 15 minutos.
            </p>
            <p>
                Se você não solicitou a alteração de senha, por favor, ignore este e-mail.
            </p>
            <p>
                Para iniciar o processo de alteração da senha, clique no botão abaixo:
           </p>
        """

    reset_link = f"{settings.RESET_PASSWORD_URL.rstrip('/')}/auth/confirmar/?code={reset_code.code}"

    button = f"""
           <a 
                href="{reset_link}"
                style="background-color: #D92B3F; 
                color: #ffffff; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px;"
            >
                Alterar Senha
            </a>
        """

    email_context = {
        'main_title': main_title,
        'body_content': body_content,
        'button': button,
        'reset_link': reset_link,
        'reset_code': reset_code.code,
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
        recipient_list=[email],
    )
