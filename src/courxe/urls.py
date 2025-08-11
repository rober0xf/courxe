from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from emails.views import email_token_login_view, logout_button_hx_view, verify_email_token_view

from .views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("", home),
    path("verify/<uuid:token>/", verify_email_token_view),
    path("hx/login/", email_token_login_view),
    path("hx/logout/", logout_button_hx_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
