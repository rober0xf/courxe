from django.contrib import admin

from .models import Email, EmailVerification

# Register your models here.

admin.site.register(Email)
admin.site.register(EmailVerification)
