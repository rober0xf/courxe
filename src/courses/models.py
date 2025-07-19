from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField
from django.db import models
from django.utils import timezone

import helpers

from .utils import id_utils, image_utils
from .utils.image_utils import handle_upload as real_handle_upload

# init the image processor
helpers.clodinary_init()


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
        if self.public_id == "" and self.public_id is None:
            self.public_id = id_utils.generate_public_id(self.title)
        super().save(*args, **kargs)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    @property
    def image_admin(self):
        if not self.image:
            return ""
        image_options = {"width": 500}
        try:
            url = CloudinaryImage(str(self.image)).build_url(**image_options)
            return url
        except Exception:
            return ""


class Lesson(models.Model):
    related_course = models.ForeignKey(Course, on_delete=models.CASCADE)  # linking the lesson with a course
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    can_preview = models.BooleanField(default=False, help_text="if the user doesnt have access to the course, can he see this?")  # type: ignore
    status = models.CharField(max_length=11, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True, null=True, resource_type="video")  # we need the resource type
    order = models.IntegerField(default=0)  # to be able to change the lessons order
    timestamp = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # feature: order of the lessons
    class Meta:
        ordering = ["order", "-updated"]  # order by most recent change
