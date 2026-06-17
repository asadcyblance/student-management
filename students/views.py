import uuid

from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from departments.models import Department
from skills.models import Skill

from .forms import StudentForm
from .models import Student, StudentTempImage
from .utils import (
    attach_temp_image_to_student,
    delete_profile_images,
    profile_image_urls,
    save_profile_images,
)


def _clear_temp_upload(request):
    token = request.session.get('student_upload_token')

    if token:
        StudentTempImage.objects.filter(upload_token=token).delete()

    request.session.pop('student_upload_token', None)


def _validate_image_upload(request):
    image_file = request.FILES.get('profile_image')

    if not image_file:
        return None, JsonResponse({
            'status': 'error',
            'message': 'No image file provided.',
        })

    if not image_file.content_type.startswith('image/'):
        return None, JsonResponse({
            'status': 'error',
            'message': 'Only image files are allowed.',
        })

    return image_file, None


def _student_detail_payload(student):
    payload = {
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
    }
    payload.update(profile_image_urls(student))
    return payload


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

    _clear_temp_upload(request)

    upload_token = str(uuid.uuid4())
    request.session['student_upload_token'] = upload_token

    form = StudentForm()

    return render(
        request,
        'students/create.html',
        {
            'form': form,
            'upload_token': upload_token,
        }
    )


@login_required
@permission_required('students.add_student', raise_exception=True)
def student_ajax_create(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            student = form.save()
            upload_token = request.POST.get('upload_token')
            attach_temp_image_to_student(student, upload_token)
            request.session.pop('student_upload_token', None)

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

        delete_profile_images(student)
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

    return JsonResponse(_student_detail_payload(student))


@login_required
@permission_required('students.add_student', raise_exception=True)
def student_ajax_upload_temp_image(request):

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    upload_token = request.POST.get('upload_token')
    session_token = request.session.get('student_upload_token')

    if not upload_token or upload_token != session_token:
        return JsonResponse({'status': 'error', 'message': 'Invalid upload session.'})

    image_file, error_response = _validate_image_upload(request)
    if error_response:
        return error_response

    StudentTempImage.objects.filter(upload_token=upload_token).delete()

    temp_image = StudentTempImage(upload_token=upload_token)
    save_profile_images(temp_image, image_file)

    return JsonResponse({
        'status': 'success',
        **profile_image_urls(temp_image),
    })


@login_required
@permission_required('students.add_student', raise_exception=True)
def student_ajax_delete_temp_image(request):

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    upload_token = request.POST.get('upload_token')
    session_token = request.session.get('student_upload_token')

    if not upload_token or upload_token != session_token:
        return JsonResponse({'status': 'error', 'message': 'Invalid upload session.'})

    StudentTempImage.objects.filter(upload_token=upload_token).delete()

    return JsonResponse({'status': 'success'})


@login_required
@permission_required('students.change_student', raise_exception=True)
def student_ajax_upload_profile(request, pk):

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    student = get_object_or_404(Student, pk=pk)

    image_file, error_response = _validate_image_upload(request)
    if error_response:
        return error_response

    save_profile_images(student, image_file)

    return JsonResponse({
        'status': 'success',
        **profile_image_urls(student),
    })


@login_required
@permission_required('students.change_student', raise_exception=True)
def student_ajax_delete_profile(request, pk):

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

    student = get_object_or_404(Student, pk=pk)
    delete_profile_images(student)
    student.save()

    return JsonResponse({'status': 'success'})


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
