import logging
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Q
from user.models import Role

logger = logging.getLogger(__name__)


def get_admin_and_dev_emails(extra_emails=None):
    User = get_user_model()
    admin_role, _ = Role.objects.get_or_create(name="Administrador")
    dev_role, _ = Role.objects.get_or_create(name="Desenvolvedor")

    emails = list(
        User.objects.filter(Q(roles=admin_role) | Q(roles=dev_role))
        .values_list('email', flat=True)
        .distinct()
    )

    if extra_emails:
        for email in extra_emails:
            if email not in emails:
                emails.append(email)

    return emails


def send_html_email(subject, recipient_list, template_path, context, from_email=None):
    try:
        html_content = render_to_string(template_path, context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            to=recipient_list
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        logger.info(f"E-mail enviado para: {recipient_list}")
        return True
    except Exception as e:
        logger.warning(f"Falha ao enviar e-mail: {str(e)}")
        return False
