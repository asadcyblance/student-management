from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Student
from .forms import StudentForm
from django.http import JsonResponse
from departments.models import Department
from skills.models import Skill


@login_required
@permission_required('students.view_student', raise_exception=True)
def student_list(request):

    students = Student.objects.all()

    return render(
        request,
        'students/list.html',
        {
            'students': students,
            'departments': Department.objects.all(),
            'skills': Skill.objects.all(),
            'gender_choices': Student.GENDER_CHOICES,
            'city_choices': Student.CITY_CHOICES,
        }
    )


@login_required
@permission_required('students.add_student', raise_exception=True)
def student_create(request):

    form = StudentForm()

    return render(
        request,
        'students/create.html',
        {
            'form': form
        }
    )


@login_required
@permission_required('students.add_student', raise_exception=True)
def student_ajax_create(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()

            return JsonResponse({
                'status': 'success',
                'id': student.id
            })

        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        })

    return JsonResponse({
        'status': 'invalid'
    })


@login_required
@permission_required('students.change_student', raise_exception=True)
def student_ajax_update(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
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
@permission_required('students.delete_student', raise_exception=True)
def student_ajax_delete(request, pk):

    if request.method == 'POST':

        student = get_object_or_404(
            Student,
            pk=pk
        )

        student.delete()

        return JsonResponse({
            'status': 'success'
        })

    return JsonResponse({
        'status': 'error'
    })


@login_required
@permission_required('students.change_student', raise_exception=True)
def student_ajax_status(request, pk):
    if request.method == 'POST':
        student = get_object_or_404(Student, pk=pk)

        status_value = request.POST.get('status')
        if status_value not in ['active', 'inactive']:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid status value'
            })

        student.is_active = (status_value == 'active')
        student.save(update_fields=['is_active'])

        return JsonResponse({
            'status': 'success',
            'is_active': student.is_active
        })

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })


@login_required
@permission_required('students.change_student', raise_exception=True)
def student_ajax_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return JsonResponse({
        'status': 'success',
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'email': student.email,
        'mobile': student.mobile,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'gender': student.gender,
        'address': student.address,
        'city': student.city,
        'department': student.department_id,
        'skills': list(student.skills.values_list('id', flat=True)),
        'is_active': student.is_active,
    })


@login_required
@permission_required('students.view_student', raise_exception=True)
def student_detail(request, pk):

    student = get_object_or_404(
        Student,
        pk=pk
    )

    return render(
        request,
        'students/detail.html',
        {
            'student': student
        }
    )
