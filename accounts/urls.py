from django.urls import path

from .views import (
    profile_image_delete,
    profile_image_load,
    profile_image_upload,
    profile_view,
)


urlpatterns = [
    path('profile/', profile_view, name='user_profile'),
    path('profile/image/upload/', profile_image_upload, name='profile_image_upload'),
    path('profile/image/delete/', profile_image_delete, name='profile_image_delete'),
    path('profile/image/load/', profile_image_load, name='profile_image_load'),
]
