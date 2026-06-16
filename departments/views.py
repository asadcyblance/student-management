from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Department
from .forms import DepartmentForm

from django.http import JsonResponse

# List all departments
def department_list(request):

    departments = Department.objects.all()

    return render(
        request,
        'departments/list.html',
        {
            'departments': departments
        }
    )


# Create a new department
def department_create(request):

    form = DepartmentForm()

    return render(
        request,
        'departments/create.html',
        {
            'form': form
        }
    )

#create with ajax
def department_ajax_create(request):

    if request.method == 'POST':

        form = DepartmentForm(request.POST)

        if form.is_valid():

            department = Department.objects.create(
                name=form.cleaned_data['name'],
                code=form.cleaned_data['code'],
                description=form.cleaned_data['description']
            )

            return JsonResponse({
                'status': 'success',
                'id': department.id,
                'name': department.name,
                'code': department.code,
                'description': department.description
            })

        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        })

    return JsonResponse({
        'status': 'invalid'
    })

#update with ajax
def department_ajax_update(request, pk):

    if request.method == 'POST':

        department = get_object_or_404(
            Department,
            pk=pk
        )

        form = DepartmentForm(request.POST)

        if form.is_valid():

            existing_department = Department.objects.filter(
                code=form.cleaned_data['code']
            ).exclude(pk=department.pk).first()

            if existing_department:
                return JsonResponse({
                    'status': 'error',
                    'errors': {
                        'code': ['Department code already exists.']
                    }
                })

            department.name = form.cleaned_data['name']
            department.code = form.cleaned_data['code']
            department.description = form.cleaned_data['description']
            department.save()

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

#delete with ajax
def department_ajax_delete(request, pk):

    if request.method == 'POST':

        department = Department.objects.get(pk=pk)

        department.delete()

        return JsonResponse({
            'status':'success'
        })

    return JsonResponse({
        'status':'error'
    })


def department_ajax_detail(request, pk):

    department = get_object_or_404(
        Department,
        pk=pk
    )

    return JsonResponse({
        'status': 'success',
        'id': department.id,
        'name': department.name,
        'code': department.code,
        'description': department.description
    })