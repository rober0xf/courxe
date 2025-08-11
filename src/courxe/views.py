from django.http import HttpRequest
from django.shortcuts import render

from emails.forms import EmailForm
from emails.services import start_verification_email

template_name = "home.html"


def home(request: HttpRequest, *args, **kwargs):
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": "",
    }

    if form.is_valid():
        email_value = form.cleaned_data.get("email")
        obj = start_verification_email(email=email_value)
        print(obj)
        context["form"] = EmailForm()  # reset the form
        context["message"] = "success, check your email"
    else:
        print(form.errors)
    return render(request, template_name, context)
