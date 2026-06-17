from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
        })
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'autofocus': True,
        }),
    )

    def clean_email(self):
        email = self.cleaned_data['email']

        if not any(self.get_users(email)):
            raise forms.ValidationError(
                'No email found in our system.'
            )

        return email
