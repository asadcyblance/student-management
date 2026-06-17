"""

URL configuration for config project.



The `urlpatterns` list routes URLs to views. For more information please see:

    https://docs.djangoproject.com/en/6.0/topics/http/urls/

"""

from django.contrib import admin

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views



from accounts.views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordResetView,
)



urlpatterns = [

    path('admin/', admin.site.urls),

    path('login/', CustomLoginView.as_view(), name='login'),

    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('departments/', include('departments.urls')),

    path('skills/', include('skills.urls')),

    path('students/', include('students.urls')),

    path('', include('dashboard.urls')),



    path(
        'password-reset/',
        CustomPasswordResetView.as_view(),
        name='password_reset',
    ),

    path(

        'password-reset/done/',

        auth_views.PasswordResetDoneView.as_view(

            template_name='accounts/password_reset_done.html',

        ),

        name='password_reset_done',

    ),

    path(

        'reset/<uidb64>/<token>/',

        auth_views.PasswordResetConfirmView.as_view(

            template_name='accounts/password_reset_confirm.html',

        ),

        name='password_reset_confirm',

    ),

    path(

        'reset/done/',

        auth_views.PasswordResetCompleteView.as_view(

            template_name='accounts/password_reset_complete.html',

        ),

        name='password_reset_complete',

    ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
