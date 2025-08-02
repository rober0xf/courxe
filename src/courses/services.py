from django.apps import apps

from .models import Course, PublishStatus


def get_published_courses():
    course = apps.get_model("courses", "Course")  # name of the app | name of the model
    return course.objects.filter(status=PublishStatus.PUBLISHED)


def get_course_detail(course_id=None):
    if course_id is None:
        return None
    obj = None
    try:
        course = apps.get_model("courses", "Course")
        course = course.objects.get(status=PublishStatus.PUBLISHED, public_id=course_id)
        obj = course
    except Exception as e:
        print(f"error: {e}")
    return obj


def get_course_lessons(course_obj: Course = None):
    lesson = apps.get_model("courses", "Lesson")
    course = apps.get_model("courses", "Course")
    lessons = lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course.lesson_set.filter(
        course__status=PublishStatus.PUBLISHED,
        status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
    )
    return lessons


def get_lesson_detail(course_id=None, lesson_id=None):
    if lesson_id or course_id is None:
        return None
    obj = None
    try:
        lesson = apps.get_model("courses", "Lesson")
        lesson = lesson.objects.get(
            course__public_id=course_id,
            course__status=PublishStatus.PUBLISHED,
            status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
            public_id=lesson_id,
        )

    except Exception as e:
        print(f"error: {e}")
    return obj
