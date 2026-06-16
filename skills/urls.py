from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.skill_list,
        name='skill_list'
    ),

    path(
        'create/',
        views.skill_create,
        name='skill_create'
    ),

    path(
        'ajax/create/',
        views.skill_ajax_create,
        name='skill_ajax_create'
    ),

    path(
        'ajax/update/<int:pk>/',
        views.skill_ajax_update,
        name='skill_ajax_update'
    ),

    path(
        'ajax/delete/<int:pk>/',
        views.skill_ajax_delete,
        name='skill_ajax_delete'
    ),

    path(
        'ajax/detail/<int:pk>/',
        views.skill_ajax_detail,
        name='skill_ajax_detail'
    ),
]