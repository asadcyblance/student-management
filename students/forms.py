from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),

            'mobile': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'required': True,
                }
            ),

            'dob': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'required': True,
                }
            ),

            'gender': forms.RadioSelect(),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'required': True,
                }
            ),

            'city': forms.Select(
                attrs={
                    'class': 'form-select',
                    'required': True,
                }
            ),

            'department': forms.Select(
                attrs={
                    'class': 'form-select',
                    'required': True,
                }
            ),

            'skills': forms.CheckboxSelectMultiple(),

            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # make all fields required
        for field in self.fields:
            self.fields[field].required = True

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']

        if len(first_name) < 3:
            raise forms.ValidationError(
                "First Name minimum 3 characters"
            )

        return first_name

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']

        if not mobile.isdigit():
            raise forms.ValidationError(
                "Only digits allowed"
            )

        if len(mobile) != 10:
            raise forms.ValidationError(
                "Mobile must be 10 digits"
            )

        return mobile

    def clean_email(self):
        email = self.cleaned_data['email']

        if Student.objects.filter(email=email).exclude(
                pk=self.instance.pk
        ).exists():

            raise forms.ValidationError(
                "Email already exists"
            )

        return email

    def clean_department(self):
        department = self.cleaned_data['department']

        if not department:
            raise forms.ValidationError(
                "Department is required"
            )

        return department

    def clean_skills(self):
        skills = self.cleaned_data['skills']

        if not skills:
            raise forms.ValidationError(
                "Select at least one skill"
            )

        return skills