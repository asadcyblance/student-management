from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.student_list,
        name='student_list'
    ),

    path(
        'create/',
        views.student_create,
        name='student_create'
    ),

    path(
        'detail/<int:pk>/',
        views.student_detail,
        name='student_detail'
    ),

    path(
        'ajax/create/',
        views.student_ajax_create,
        name='student_ajax_create'
    ),

    path(
        'ajax/update/<int:pk>/',
        views.student_ajax_update,
        name='student_ajax_update'
    ),

    path(
        'ajax/delete/<int:pk>/',
        views.student_ajax_delete,
        name='student_ajax_delete'
    ),

    path(
        'ajax/detail/<int:pk>/',
        views.student_ajax_detail,
        name='student_ajax_detail'
    ),

    path(
        'ajax/status/<int:pk>/',
        views.student_ajax_status,
        name='student_ajax_status'
    ),

    path(
        'ajax/upload-temp-image/',
        views.student_ajax_upload_temp_image,
        name='student_ajax_upload_temp_image'
    ),

    path(
        'ajax/delete-temp-image/',
        views.student_ajax_delete_temp_image,
        name='student_ajax_delete_temp_image'
    ),

    path(
        'ajax/upload-profile/<int:pk>/',
        views.student_ajax_upload_profile,
        name='student_ajax_upload_profile'
    ),

    path(
        'ajax/delete-profile/<int:pk>/',
        views.student_ajax_delete_profile,
        name='student_ajax_delete_profile'
    ),
]