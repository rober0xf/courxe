from cloudinary.utils import cloudinary_url
from django.template.loader import get_template

from courxe import settings


def set_sizes(obj, height=None, width=None):
    if height is not None:
        obj["height"] = height
    if width is not None:
        obj["width"] = width
    if height and width:
        obj["crop"] = "fill"


def get_cloudinary_image_object(instance, field_name="image", as_html=False, height=None, width=None):
    if not hasattr(instance, field_name):
        return ""

    image_object = getattr(instance, field_name)
    if not image_object:
        return ""

    image_options = {
        "resource_type": "image",
        "fetch_format": "auto",
        "qualityt": "auto",
    }
    set_sizes(obj=image_options, height=height, width=width)

    try:
        if as_html:
            url, options = cloudinary_url(str(image_object), **image_options)
            img_attrs = f"width='{width}'" if width else ""
            img_attrs += f"height='{height}'" if height else ""
            return f"<img src='{url}' {img_attrs} alt='Image' style='max-width: 100%; height: auto;'>"
        else:
            url, _ = cloudinary_url(str(image_object), **image_options)
            return url
    except Exception as e:
        print(f"error generating image: {e}")
        return ""


def get_cloudinary_video_object(
    instance,
    field_name="video",
    as_html=False,
    width=None,
    height=None,
    fetch_format="auto",
    quality="auto",
    controls=True,
    autoplay=False,
):
    if not hasattr(instance, field_name):
        return ""

    video_object = getattr(instance, field_name)
    if not video_object:
        return ""

    video_options = {
        "resource_type": "video",
        "fetch_format": fetch_format,
        "quality": quality,
        "type": "private",
        "sign_url": True,
    }

    set_sizes(obj=video_options, height=height, width=width)

    try:
        url, _ = cloudinary_url(str(video_object), **video_options)
        if as_html:
            template = get_template("videos/snippets/video_embed.html")
            html = template.render(
                {
                    "video_url": url,
                    "cloudinary_name": settings.CLOUDINARY_CLOUD_NAME,
                    "controls": controls,
                    "autoplay": autoplay,
                    "width": width,
                    "height": height,
                }
            )
            return html

        return url
    except Exception as e:
        print("error generating video: ", e)
        return ""
