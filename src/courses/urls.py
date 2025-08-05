from django.urls import path

from .views import course_detail_view, course_list_view, lesson_detail_view

urlpatterns = [
    path("", course_list_view),
    path("<slug:course_id>/", course_detail_view),  # we need to pass what parameter it expects
    path("<slug:course_id>/lessons/<int:lesson_id>/", lesson_detail_view),
]
