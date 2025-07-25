from typing import cast

from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone

import helpers

from .utils import id_utils, image_utils
from .utils.image_utils import handle_upload as real_handle_upload

# init the image processor
helpers.cloudinary_init()


# we need to define here so django dont complain, real_handle_upload has the correct logic
def handle_upload(instance, filename):
    return real_handle_upload(instance, filename)


class AcessRequirements(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email Required"


class PublishStatus(models.TextChoices):
    # the lowercase one its how it will be stored in the db, and the capitalized one its how it will be displayed to the user.
    PUBLISHED = "published", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=120, blank=True, null=True)  # slug
    image = CloudinaryField(  # better to use cloudinaryfield than imagefield
        "image",
        null=True,
        public_id_prefix=id_utils.get_public_id_prefix,
        display_name=image_utils.get_display_name,
        tags=["course", "thumbnail"],
    )
    access = models.CharField(max_length=14, choices=AcessRequirements.choices, default=AcessRequirements.ANYONE)
    status = models.CharField(max_length=11, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    def save(self, *args, **kargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = id_utils.generate_public_id(self)  # self.title would be wrong
        super().save(*args, **kargs)

    def get_display_name(self):
        return f"{self.title}"

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    @property
    def path(self):
        if not self.public_id:
            raise ValueError("public_id is not set")
        return f"/courses/{self.public_id}/"


class Lesson(models.Model):
    related_course = models.ForeignKey(Course, on_delete=models.CASCADE)  # linking the lesson with a course
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=120, blank=True, null=True)  # slug
    can_preview = models.BooleanField(default=False, help_text="if the user doesnt have access to the course, can he see this?")  # type: ignore
    status = models.CharField(max_length=11, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    thumbnail = CloudinaryField(
        "image",
        public_id_prefix=id_utils.get_public_id_prefix,
        display_name=image_utils.get_display_name,
        blank=True,
        null=True,
    )
    video = CloudinaryField(
        "video",
        public_id_prefix=id_utils.get_public_id_prefix,
        display_name=image_utils.get_display_name,
        blank=True,
        null=True,
        resource_type="video",
        type="upload",
    )  # we need the resource type
    order = models.IntegerField(default=0)  # to be able to change the lessons order
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # feature: order of the lessons
    class Meta:
        ordering = ["order", "-updated"]  # order by most recent change

    def save(self, *args, **kargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = id_utils.generate_public_id(self)
        super().save(*args, **kargs)

    def get_display_name(self):
        if not self.related_course or not hasattr(self.related_course, "get_display_name"):
            raise ValueError("related_course or its get_display_name is not set")

        course = cast(Course, self.related_course)  # for lsp reason
        return f"{self.title}-{course.get_display_name()}"

    @property
    def path(self):
        if not self.related_course or not hasattr(self.related_course, "path"):
            raise ValueError("related_course or its path is not set")
        if not self.public_id:
            raise ValueError("public_id is not set")

        course = cast(Course, self.related_course)  # for lsp reason
        course_path = str(course.path)
        if course_path.endswith("/"):
            course_path = course_path[:-1]

        return f"{course_path}/lessons/{self.public_id}"
