from typing import cast

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.utils import timezone

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


def verify_email_token(token, max_attemps=5):
    queryset: QuerySet[EmailVerification] = EmailVerification.objects.filter(token=token)

    if not queryset.exists() and not queryset.count() == 1:
        return False, "invalid token"
    is_email_expired = queryset.filter(expired=True)
    if not is_email_expired.exists():
        return False, "token expired, try again"

    max_attempts_reached = queryset.filter(attempts__gte=max_attemps)
    if max_attempts_reached.exists():
        return False, "token expired, used too many times"

    obj = cast(EmailVerification | None, queryset.first())

    if obj is None:
        return False, "object is none"

    obj.attempts += 1
    obj.last_attempt_at = timezone.now()

    if obj.attempts > max_attemps:
        obj.expired = True
        obj.expired_at = timezone.now()
    obj.save()

    return True, "welcome"
