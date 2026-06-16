from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from students.models import Student
from departments.models import Department
from skills.models import Skill


@login_required
def dashboard(request):

    context = {
        'student_count': Student.objects.count(),
        'department_count': Department.objects.count(),
        'skill_count': Skill.objects.count(),
        'active_students': Student.objects.filter(is_active=True).count(),
        'inactive_students': Student.objects.filter(is_active=False).count(),
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )
