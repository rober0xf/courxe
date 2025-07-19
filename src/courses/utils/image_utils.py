def handle_upload(instance: str, filename):
    return f"filename: {filename}"


def get_display_name(instance, *args, **kargs):
    if hasattr(instance, "get_display_name"):
        return instance.get_display_name()
    elif hasattr(instance, "title"):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} upload"
