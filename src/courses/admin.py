from django.contrib import admin
from django.utils.html import format_html

from .models import Course, Lesson


# show lessons
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0  # to not show empty lessons
    readonly_fields = ["updated"]  # so we can only see it


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["title", "status", "access"]
    list_filter = ["access", "status"]
    fields = ["title", "description", "access", "status", "image", "display_image", "public_id"]
    readonly_fields = ["public_id", "display_image"]  # we need to create display image here because its not a field of the course model

    def display_image(self, obj, *args, **kwargs):
        # object its the instance of the course
        url = obj.image_admin
        return format_html("<img src='{}' />", url)
