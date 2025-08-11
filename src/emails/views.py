from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django_htmx.http import HttpResponseClientRedirect

from emails.forms import EmailForm

from .services import start_verification_email, verify_email_token


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

    next_url = request.session.get("next_url") or "/"
    if not next_url.startswith("/"):
        next_url = "/"

    return redirect(next_url)


def email_token_login_view(request: HttpRequest):
    if not request.META.get("HTTP_HX_REQUEST"):
        return redirect("/")

    email_id_in_session = request.session.get("email_id")
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": "",
        "show_form": not email_id_in_session,
    }

    template_name = "emails/hx/form.html"
    if form.is_valid():
        email_value = form.cleaned_data.get("email")
        obj = start_verification_email(email=email_value)
        print(obj)
        context["form"] = EmailForm()  # reset the form
        context["message"] = "success, check your email"
        return HttpResponseClientRedirect("/welcome")
    else:
        print(form.errors)
    return render(request, template_name, context)


def logout_button_hx_view(request: HttpRequest):
    if not request.META.get("HTTP_HX_REQUEST"):
        return redirect("/")

    if request.method == "post":
        try:
            del request.session["email_id"]
        except Exception:
            pass

        email_id_in_session = request.session.get("email_id")
        if not email_id_in_session:
            return HttpResponseClientRedirect("/")

    return render(request, "/emails/hx/logout-btn.html", {})
