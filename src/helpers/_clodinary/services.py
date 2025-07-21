from cloudinary import CloudinaryImage, CloudinaryVideo


def set_sizes(obj, height=None, width=None):
    if height is not None:
        obj["height"] = height
    if width is not None:
        obj["width"] = width
    if height and width:
        obj["crop"] = "limit"


def get_cloudinary_image_object(instance, field_name="image", as_html=False, width=None):
    if not hasattr(instance, field_name):
        return ""

    image_object = getattr(instance, field_name)
    if not image_object:
        return ""

    image_options = {}
    set_sizes(obj=image_options, width=width)

    try:
        if as_html:
            return image_object.image(**image_options)
        url = CloudinaryImage(str(image_object)).build_url(**image_options)
        return url
    except Exception:
        return ""


def get_cloudinary_video_object(
    instance,
    field_name="video",
    as_html=False,
    width=None,
    height=None,
    is_private=False,
    fetch_format="auto",
    quality="auto",
):
    if not hasattr(instance, field_name):
        return ""

    video_object = getattr(instance, field_name)
    if not video_object:
        return ""

    video_options = {
        "is_priv": is_private,
        "fetch_format": fetch_format,
        "quality": quality,
    }
    set_sizes(obj=video_options, height=height, width=width)

    try:
        if as_html:
            return video_object.video(**video_options)
        url = CloudinaryVideo(str(video_object)).build_url(**video_options)
        return url
    except Exception:
        return ""
