def handle_upload(instance: str, filename):
    return f"filename: {filename}"


def get_display_name(instance, *args, **kargs):
    title = instance.title
    if title:
        return title
    return "Course upload"
