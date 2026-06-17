from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.http import FileResponse
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import (
    CustomLoginForm,
    CustomPasswordResetForm,
    UserProfileForm,
    UserUpdateForm,
)
from .models import UserProfile

ALLOWED_LOGIN_GROUPS = ('Admin', 'Staff')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()

        if user.is_superuser or user.groups.filter(
            name__in=ALLOWED_LOGIN_GROUPS
        ).exists():
            return super().form_valid(form)

        messages.error(
            self.request,
            'You do not have access to this system. Contact superuser.'
        )
        return redirect('login')


class CustomLogoutView(LogoutView):
    next_page = 'login'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']

        if not any(form.get_users(email)):
            form.add_error(
                'email',
                'No email found in our system.',
            )
            return self.form_invalid(form)

        return super().form_valid(form)


def _get_password_form(user, data=None):
    form = PasswordChangeForm(user, data=data)
    for field in form.fields.values():
        field.widget.attrs.update({'class': 'form-control'})
    return form


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_form = UserUpdateForm(instance=request.user)
    profile_form = UserProfileForm(instance=profile)
    password_form = _get_password_form(request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'profile':
            user_form = UserUpdateForm(
                request.POST,
                instance=request.user,
            )
            profile_form = UserProfileForm(
                request.POST,
                request.FILES,
                instance=profile,
            )

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('user_profile')

        elif action == 'password':
            password_form = _get_password_form(
                request.user,
                data=request.POST,
            )

            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')
                return redirect('user_profile')

    return render(
        request,
        'accounts/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'password_form': password_form,
            'filepond_initial_file': (
                profile.profile_image.url if profile.profile_image else ''
            ),
        },
    )


@login_required
@require_POST
def profile_image_upload(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    uploaded_file = request.FILES.get('profile_image') or request.FILES.get('filepond')

    if not uploaded_file:
        return JsonResponse({'error': 'No file received.'}, status=400)

    profile.clear_images()
    profile.profile_image = uploaded_file
    profile.save()

    return HttpResponse(profile.profile_image.name, status=201, content_type='text/plain')


@login_required
@require_http_methods(['DELETE', 'POST'])
def profile_image_delete(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not profile.profile_image:
        return JsonResponse({'status': 'empty'}, status=200)

    profile.clear_images()
    return JsonResponse({'status': 'deleted'}, status=200)


@login_required
def profile_image_load(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if not profile.profile_image:
        return JsonResponse({'error': 'No profile image found.'}, status=404)

    return FileResponse(profile.profile_image.open('rb'))
