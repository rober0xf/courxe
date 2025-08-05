from django import forms

from .css import EMAIL_FIELD_CSS
from .services import verify_email


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "id": "email-login-input",
                "class": EMAIL_FIELD_CSS,
                "placeholder": "your email",
            },
        )
    )

    # class Meta:
    #     model = EmailVerification
    #     fields: list[str] = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        verified = verify_email(email=email)
        if not verified:
            raise forms.ValidationError("invalid email")
        return email
