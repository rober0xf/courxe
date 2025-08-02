from django.http import Http404, HttpResponse
from django.shortcuts import render

from src.helpers import get_cloudinary_video_object

from .services import get_course_detail, get_course_lessons, get_lesson_detail, get_published_courses


# Create your views here.
def course_list_view(request: HttpResponse):
    queryset = get_published_courses()
    # return JsonResponse({"data": [x.path for x in queryset]})
    context = {"object_list": queryset}
    return render(request, "courses/list.html", context)


def course_detail_view(request: HttpResponse, course_id=None, *args, **kwargs):
    course_obj = get_course_detail(course_id)
    if course_obj is None:
        raise Http404
    lesson_queryset = get_course_lessons(course_obj)
    # return JsonResponse({"data": course_obj.id, "lesson_ids": [lesson.id for lesson in lesson_queryset]})
    context = {
        "object": course_obj,
        "lesson_queryset": lesson_queryset,
    }
    return render(request, "courses/detail.html", context)


def lesson_detail_view(request: HttpResponse, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = get_lesson_detail(course_id, lesson_id)
    if lesson_obj is None:
        raise Http404

    template = "/courses/lesson-coming-soon.html"
    context = {"object": lesson_obj}
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        """ lesson in published, keep going """
        """video is available"""
        template = "courses/lesson.html"
        video_embed_html = get_cloudinary_video_object(
            instance=lesson_obj,
            field_name="video",
            as_html=True,
            height=450,
            width=500,
            autoplay=False,
            controls=True,
        )
        context["video_embed"] = video_embed_html

    return render(request, template, context)
