import os
from io import BytesIO

# utils.py
from PIL import Image
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string


def random_string(length=18):
    return get_random_string(length)


def get_file_name(file_name):
    """
    _Get File Name_
    Args:
    file_name (_str_): Name file (image, movie, etc.)
    Returns:
    _tuple_: Name and ext
    """
    base_name = os.path.basename(file_name)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance=None, filename=None):
    """
    _Upload Image Path_
    Args:
    instance (django obj instance, optional): The object that the file is for. Defaults to None.
    filename (_type_, optional): The final generated name for the file. Defaults to None.
    Returns:
    _str_: Final path and file name
    """
    model_name = instance.__class__.__name__.lower()
    name, ext = get_file_name(filename)
    return f"{model_name}/{random_string()}/{name}{ext}"


def create_thumbnail(image_field, size=(566, 478)):
    """
    Create a thumbnail from an ImageField
    """
    # Open the image
    img = Image.open(image_field)

    # Convert to RGB (this is necessary for some image formats like PNG)
    img = img.convert('RGB')

    # Resize the image
    img = img.resize(size, Image.Resampling.LANCZOS)

    # Prepare a BytesIO object to save the image
    thumb_io = BytesIO()

    # Determine the format
    format_image = image_field.name.split('.')[-1].lower()
    if format_image in ['jpg', 'jpeg', 'jfif']:
        format_image = 'JPEG'
    elif format_image == 'png':
        format_image = 'PNG'
    else:
        format_image = 'JPEG'  # Default to JPEG for other formats

    # Save the image to the BytesIO object
    img.save(thumb_io, format=format_image, quality=85)

    # Seek to the beginning of the BytesIO object
    thumb_io.seek(0)
    thumbnail = ContentFile(thumb_io.getvalue(), name=f"thumb_{image_field.name}")
    return thumbnail
