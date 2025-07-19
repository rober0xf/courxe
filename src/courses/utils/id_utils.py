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
    if hasattr(instance, "path"):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_slug = slugify(model_name)
    if not public_id:
        return f"{model_slug}"
    return f"{model_slug}/{public_id}"
