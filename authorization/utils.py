from django.core.mail import send_mail
from django.core.mail.message import EmailMessage

def send_custom_email(subject, message, from_email, recipient_list, user):
    user_info = f"\n\nEnviado por:\nNome de Usuário: {user.username}\nEndereço de E-mail: {user.email}"
    full_message = f"{message}{user_info}"

    email = EmailMessage(
        subject,
        full_message,
        from_email,
        recipient_list
    )
    return email.send(fail_silently=False)