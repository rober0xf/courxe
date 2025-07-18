from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "access"]
    list_filter = ["access", "status"]
    readonly_fields = ["display_image"]  # we need to create display image here because its not a field of the course model
    fields = ["title", "description", "access", "status", "image", "display_image"]

    def display_image(self, object, *args, **kwargs):
        # object its the instance of the course
        cloudinary_id = str(object.image)
        cloudinary_image = CloudinaryImage(cloudinary_id).image(width=500)
        return format_html(cloudinary_image)
