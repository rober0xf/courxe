from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect

from .services import verify_email_token


# Create your views here.
def verify_email_token_view(request: HttpRequest, token, *args, **kwargs):
    is_verified, msg, email_obj = verify_email_token(token)
    if not is_verified:
        try:
            del request.session["email_id"]
        except Exception as _:
            pass

        messages.error(request, msg)
        return redirect("/login/")

    messages.success(request, msg)
    if email_obj is not None:
        request.session["email_id"] = f"{email_obj.id}"

    return redirect("/")
