import os
from django.conf import settings
from emails.send_email import send_html_email


def send_ticket_email_to_user(context, recipient_email):

    template = os.path.join(
        settings.EMAIL_TEMPLATES_DIR,
        'request_analyzed.html'
    )

    subject = "Sua sugestão foi analisada"

    send_html_email(
        subject=subject,
        template_path=template,
        context=context,
        recipient_list=[recipient_email],
    )
