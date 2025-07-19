from uuid import uuid4

from django.utils.text import slugify


def generate_public_id(instance, *args, **kargs):
    title = instance.title
    unique_id = str(uuid4()).replace("-", "")
    if not title:
        return unique_id
    shorted = unique_id[0:5]  # we create a short id bc a same course can have multiple lessons with the same slug name
    slug = slugify(title)
    return f"{slug}-{shorted}"


# for the image url field
def get_public_id_prefix(instance, *args, **kargs):
    title = instance.title
    if title:
        slug = slugify(title)
        unique_id = str(uuid4()).replace("-", "")[:5]
        return f"courses/{slug}-{unique_id}-"  # url will be like www.yari/courses-id-yara
    if instance.id:
        return f"courses/{instance.id}"
    return "courses"
