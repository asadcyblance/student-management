from django import forms


class DepartmentForm(forms.Form):

    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    code = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 4
            }
        )
    )

    def clean_name(self):

        name = self.cleaned_data['name']

        if len(name) < 3:
            raise forms.ValidationError(
                'Department name must be at least 3 characters.'
            )

        return name

    def clean_code(self):

        code = self.cleaned_data['code']

        if len(code) < 3:
            raise forms.ValidationError(
                'Department code must be at least 3 characters.'
            )

        return code

    def clean_description(self):

        description = self.cleaned_data['description']

        if len(description) < 10:
            raise forms.ValidationError(
                'Department description must be at least 10 characters.'
            )

        return description  