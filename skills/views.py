from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Skill
from .forms import SkillForm
from django.http import JsonResponse

# List all skills
def skill_list(request):

    skills = Skill.objects.all()

    return render(
        request,
        'skills/list.html',
        {
            'skills': skills
        }
    )

# Create a new skill
def skill_create(request):

    form = SkillForm()

    return render(
        request,
        'skills/create.html',
        {
            'form': form
        }
    )

# create with ajax
def skill_ajax_create(request):

    if request.method == 'POST':

        form = SkillForm(request.POST)

        if form.is_valid():

            skill = form.save()

            return JsonResponse({
                'status': 'success',
                'id': skill.id,
                'name': skill.name,
                'description': skill.description
            })

        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        })

    return JsonResponse({
        'status': 'invalid'
    })

# update with ajax
def skill_ajax_update(request, pk):

    skill = get_object_or_404(
        Skill,
        pk=pk
    )

    if request.method == 'POST':

        form = SkillForm(
            request.POST,
            instance=skill
        )

        if form.is_valid():

            form.save()

            return JsonResponse({
                'status': 'success'
            })

        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        })

    return JsonResponse({
        'status': 'invalid'
    })

# delete with ajax
def skill_ajax_delete(request, pk):

    if request.method == 'POST':

        skill = get_object_or_404(
            Skill,
            pk=pk
        )

        skill.delete()

        return JsonResponse({
            'status': 'success'
        })

    return JsonResponse({
        'status': 'error'
    })


def skill_ajax_detail(request, pk):

    skill = get_object_or_404(
        Skill,
        pk=pk
    )

    return JsonResponse({
        'status': 'success',
        'id': skill.id,
        'name': skill.name,
        'description': skill.description
    })