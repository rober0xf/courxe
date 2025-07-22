from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

import helpers

from .models import Course, Lesson


# show lessons
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0  # to not show empty lessons
    # so we can only see it
    readonly_fields = [
        "public_id",
        "updated",
        "display_image",
        "display_video",
    ]

    def display_image(self, obj):
        if not obj.thumbnail:
            return format_html("no thumbnail")

        try:
            image_html = helpers.get_cloudinary_image_object(
                instance=obj,
                field_name="thumbnail",
                as_html=True,
                width=200,
                height=150,
            )
            return mark_safe(image_html)

        except Exception as e:
            return format_html(f"error: {e}")

    display_image.short_description = "thumbnail Preview"

    def display_video(self, obj, *args, **kwargs):
        if not obj.video:
            return format_html("no video")

        try:
            video_embed_html = helpers.get_cloudinary_video_object(
                instance=obj,
                field_name="video",
                as_html=True,
                height=450,
                width=500,
                autoplay=False,
                controls=True,
            )
            return mark_safe(video_embed_html)
        except Exception as e:
            return format_html(f"error: {e}")

    display_video.short_description = "video Preview"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["title", "status", "access", "display_image"]
    list_filter = ["access", "status"]
    search_fields = ["title", "description", "access", "status", "image", "display_image", "public_id"]
    readonly_fields = ["public_id", "display_image"]  # we need to create display image here because its not a field of the course model

    def display_image(self, obj, *args, **kwargs):
        # object its the instance of the course
        if not obj.image:
            return "no image"

        try:
            image_html = helpers.get_cloudinary_image_object(
                instance=obj,
                field_name="image",
                as_html=True,
                height=100,
                width=150,
            )
            return mark_safe(image_html)
        except Exception as e:
            return f"error: {e}"

    display_image.short_description = "image preview"
