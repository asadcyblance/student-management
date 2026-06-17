from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.shortcuts import redirect

from .forms import CustomLoginForm, CustomPasswordResetForm

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
