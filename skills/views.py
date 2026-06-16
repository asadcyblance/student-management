from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Skill
from .forms import SkillForm
from django.http import JsonResponse


@login_required
@permission_required('skills.view_skill', raise_exception=True)
def skill_list(request):

    skills = Skill.objects.all()

    return render(
        request,
        'skills/list.html',
        {
            'skills': skills
        }
    )


@login_required
@permission_required('skills.add_skill', raise_exception=True)
def skill_create(request):

    form = SkillForm()

    return render(
        request,
        'skills/create.html',
        {
            'form': form
        }
    )


@login_required
@permission_required('skills.add_skill', raise_exception=True)
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


@login_required
@permission_required('skills.change_skill', raise_exception=True)
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


@login_required
@permission_required('skills.delete_skill', raise_exception=True)
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


@login_required
@permission_required('skills.change_skill', raise_exception=True)
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
