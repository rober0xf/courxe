from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from emails.views import verify_email_token_view

from .views import home

urlpatterns = [
    path(route="admin/", view=admin.site.urls),
    path("courses/", include("courses.urls")),
    path(route="", view=home),
    path("verify/<uuid:token>/", verify_email_token_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
