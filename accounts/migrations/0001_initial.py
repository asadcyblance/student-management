import accounts.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to=accounts.models.profile_image_upload_path)),
                ('profile_thumb', models.ImageField(blank=True, null=True, upload_to='profiles/thumb/')),
                ('profile_medium', models.ImageField(blank=True, null=True, upload_to='profiles/medium/')),
                ('profile_large', models.ImageField(blank=True, null=True, upload_to='profiles/large/')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
