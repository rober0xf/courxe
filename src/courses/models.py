from cloudinary.models import CloudinaryField
from django.db import models

import helpers

# init the image processor
helpers.clodinary_init()


def handle_upload(instance: str, filename):
    return f"filename: {filename}"


class AcessRequirements(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email_required", "Email Required"


class PublishStatus(models.TextChoices):
    # the lowercase one its how it will be stored in the db, and the capitalized one its how it will be displayed to the user.
    PUBLISHED = "published", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


class Course(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField("image", null=True)
    access = models.CharField(max_length=14, choices=AcessRequirements.choices, default=AcessRequirements.ANYONE)
    status = models.CharField(max_length=11, choices=PublishStatus.choices, default=PublishStatus.DRAFT)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
