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
]