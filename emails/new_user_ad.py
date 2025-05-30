import os
from django.conf import settings
from emails.send_email import send_html_email


def send_new_user_ad(reset_code,  email):

    subject = "Seu cadastro foi realizado com sucesso!"

    main_title = "Bem vindo ao CMR!"

    body_content = f"""
            <p>
                Prezado(a) usuário(a), seja bem-vindo(a) ao CMR!
                Seu cadastro foi realizado com sucesso.
            </p>
            <p>
                Para acessar sua conta você deve utilizar o seu email e senha que você utiliza no AD (Active Directory) da sua instituição, clique no botão abaixo acessar o sistema:
            </p>
        """

    reset_link = f"{settings.RESET_PASSWORD_URL.rstrip('/')}"

    button = f"""
           <a 
                href="{reset_link}"
                style="background-color: #D92B3F; 
                color: #ffffff; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px;"
            >
                Acessar o sistema
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
