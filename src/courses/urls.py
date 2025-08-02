from django.urls import path

from .views import course_detail_view, course_list_view, lesson_detail_view

urlpatterns = [
    path(route="/", view=course_list_view),
    path(route="<slug:course_id>/", view=course_detail_view),  # we need to pass what parameter it expects
    path(route="<slug:course_id>/lessons/<int:lesson_id>/", view=lesson_detail_view),
]
