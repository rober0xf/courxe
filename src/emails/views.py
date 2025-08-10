from django.http import HttpResponse

from .services import verify_email_token


# Create your views here.
def verify_email_token_view(request, token, *args, **kwargs):
    is_verified, msg = verify_email_token(token)
    if not is_verified:
        return HttpResponse(msg)
    return HttpResponse(token)
