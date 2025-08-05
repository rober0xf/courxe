from django.conf import settings
from django.core.mail import send_mail

from .models import Email, EmailVerification

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def verify_email(email):
    query_set = Email.objects.filter(email=email)
    return query_set.exists()


def get_verification_email_message(verification_instance: EmailVerification, as_html=False):
    if not isinstance(verification_instance, EmailVerification):
        return None

    verify_link = verification_instance.get_link()
    if as_html:
        return f"<h1>{verify_link}</h1>"
    return f"{verify_link}"


def start_verification_email(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerification.objects.create(parent=email_obj, email=email)
    sent = send_verification_email(obj.id)
    return obj, sent


def send_verification_email(obj_id):
    obj = EmailVerification.objects.get(id=obj_id.id)
    email = obj_id.email
    subject = "verify your email"
    from_user = EMAIL_HOST_USER
    text_html = get_verification_email_message(obj, as_html=True)
    text_message = get_verification_email_message(obj, as_html=False)

    sent = send_mail(
        subject=subject,
        message=text_message,
        from_email=from_user,
        recipient_list=[email],
        fail_silently=False,
        html_message=text_html,
    )
    return sent
