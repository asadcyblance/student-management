from io import BytesIO
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image


def profile_image_upload_path(instance, filename):
    extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    return f'profiles/original/user_{instance.user_id}_{uuid4().hex}.{extension}'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    profile_image = models.ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True,
    )
    profile_thumb = models.ImageField(
        upload_to='profiles/thumb/',
        blank=True,
        null=True,
    )
    profile_medium = models.ImageField(
        upload_to='profiles/medium/',
        blank=True,
        null=True,
    )
    profile_large = models.ImageField(
        upload_to='profiles/large/',
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Profile: {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.profile_image:
            self._create_resized_images()

    def _create_resized_images(self):
        size_map = {
            'profile_thumb': (100, 100),
            'profile_medium': (300, 300),
            'profile_large': (600, 600),
        }

        # Open once from storage and generate each variant.
        with self.profile_image.open('rb') as image_file:
            source = Image.open(image_file).convert('RGB')

            for field_name, size in size_map.items():
                resized = source.copy()
                resized.thumbnail(size, Image.Resampling.LANCZOS)

                image_io = BytesIO()
                resized.save(image_io, format='JPEG', quality=90)
                image_content = ContentFile(image_io.getvalue())

                original_name = self.profile_image.name.rsplit('/', 1)[-1].rsplit('.', 1)[0]
                file_name = f'user_{self.user_id}_{field_name}_{original_name}.jpg'

                getattr(self, field_name).save(file_name, image_content, save=False)

        super().save(update_fields=['profile_thumb', 'profile_medium', 'profile_large'])

    def clear_images(self):
        image_fields = [
            'profile_image',
            'profile_thumb',
            'profile_medium',
            'profile_large',
        ]

        for field_name in image_fields:
            image_field = getattr(self, field_name)
            if image_field:
                image_field.delete(save=False)
                setattr(self, field_name, None)

        self.save(update_fields=image_fields)
