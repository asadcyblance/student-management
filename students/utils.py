import uuid

from django.core.files import File
from django.core.files.base import ContentFile
from io import BytesIO

from PIL import Image


IMAGE_SIZES = {
    'thumb': (150, 150),
    'medium': (400, 400),
    'large': (800, 800),
}

PROFILE_FIELDS = ('profile_thumb', 'profile_medium', 'profile_large')


def generate_image_variants(image_file):
    image = Image.open(image_file)

    if image.mode in ('RGBA', 'P'):
        image = image.convert('RGB')

    variants = {}

    for size_name, dimensions in IMAGE_SIZES.items():
        copy = image.copy()
        copy.thumbnail(dimensions, Image.Resampling.LANCZOS)
        buffer = BytesIO()
        copy.save(buffer, format='JPEG', quality=85)
        buffer.seek(0)
        filename = f'{uuid.uuid4().hex}.jpg'
        variants[size_name] = ContentFile(buffer.read(), name=filename)

    return variants


def save_profile_images(instance, image_file):
    variants = generate_image_variants(image_file)

    for size_name, content_file in variants.items():
        field_name = f'profile_{size_name}'
        field = getattr(instance, field_name)

        if field:
            field.delete(save=False)

        field.save(content_file.name, content_file, save=False)

    instance.save()


def delete_profile_images(instance):
    for field_name in PROFILE_FIELDS:
        field = getattr(instance, field_name, None)

        if field:
            field.delete(save=False)


def attach_temp_image_to_student(student, upload_token):
    if not upload_token:
        return

    from .models import StudentTempImage

    try:
        temp_image = StudentTempImage.objects.get(upload_token=upload_token)
    except StudentTempImage.DoesNotExist:
        return

    for size_name in IMAGE_SIZES:
        temp_field = getattr(temp_image, f'profile_{size_name}')
        student_field = getattr(student, f'profile_{size_name}')

        if not temp_field:
            continue

        with temp_field.open('rb') as file_handle:
            student_field.save(
                temp_field.name.split('/')[-1],
                File(file_handle),
                save=False,
            )

    student.save()
    temp_image.delete()


def profile_image_urls(instance):
    urls = {}

    for size_name in IMAGE_SIZES:
        field = getattr(instance, f'profile_{size_name}', None)
        urls[size_name] = field.url if field else None

    return urls
