from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.department_list,
        name='department_list'
    ),

    path(
        'create/',
        views.department_create,
        name='department_create'
    ),

    path(
    'ajax/create/',
    views.department_ajax_create,
    name='department_ajax_create'
    ),

    path(
        'ajax/update/<int:pk>/',
        views.department_ajax_update,
        name='department_ajax_update'
    ),

    path(
        'ajax/delete/<int:pk>/',
        views.department_ajax_delete,
        name='department_ajax_delete'
    ),

    path(
        'ajax/detail/<int:pk>/',
        views.department_ajax_detail,
        name='department_ajax_detail'
    ),
]