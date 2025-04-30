import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from user.models import Role
from send_email import send_html_email


def send_ticket_email_to_admins(context):

    admin_template = os.path.join(
        settings.EMAIL_TEMPLATES_DIR,
        'request_analyzed_adm.html'
    )

    subject = "Nova sugestão analisada"

    admin_role, _ = Role.objects.get_or_create(name="Administrador")
    dev_role, _ = Role.objects.get_or_create(name="Desenvolvedor")

    User = get_user_model()
    admin_emails = list(
        User.objects.filter(Q(roles=admin_role) | Q(roles=dev_role))
        .values_list('email', flat=True)
        .distinct()
    )

    if admin_emails:
        send_html_email(
            subject=subject,
            template_path=admin_template,
            context=context,
            recipient_list=admin_emails,
        )
