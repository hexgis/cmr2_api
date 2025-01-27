from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_custom_email(
    subject: str,
    recipients: list,
    template_path: str,
    context: dict,
    from_email: str = 'hexgisdev@gmail.com',
    attachments: list = None,
):
    """
    Envia um e-mail customizado usando EmailMultiAlternatives.

    Args:
        subject (str): Assunto do e-mail.
        recipients (list): Lista de destinatários.
        template_path (str): Caminho para o template HTML.
        context (dict): Contexto para renderizar o template.
        from_email (str): E-mail do remetente.
        attachments (list): Lista de anexos no formato [(filename, content, mimetype)].

    Returns:
        bool: True se o e-mail foi enviado com sucesso.
    """
    try:
        # Renderiza o conteúdo HTML
        html_content = render_to_string(template_path, context)

        # Cria o objeto de e-mail
        email = EmailMultiAlternatives(
            subject=subject,
            body='Este e-mail contém conteúdo em HTML. Verifique sua compatibilidade.',  # Texto alternativo.
            from_email=from_email,
            to=recipients,
        )

        # Adiciona a versão HTML
        email.attach_alternative(html_content, 'text/html')

        # Adiciona anexos, se existirem
        if attachments:
            for filename, content, mimetype in attachments:
                email.attach(filename, content, mimetype)

        # Envia o e-mail
        email.send()
        return True

    except Exception as e:
        # Log ou tratamento de erro
        print(f"Erro ao enviar e-mail: {e}")
        return False
