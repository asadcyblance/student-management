from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect

from .forms import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()

        if user.is_superuser or user.groups.filter(name='Admin').exists():
            return super().form_valid(form)

        messages.error(
            self.request,
            'You do not have access to this system. Contact superuser.'
        )
        return redirect('login')


class CustomLogoutView(LogoutView):
    next_page = 'login'
