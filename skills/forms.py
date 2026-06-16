from django import forms

from .models import Skill


class SkillForm(forms.ModelForm):

    class Meta:

        model = Skill

        fields = [
            'name',
            'description'
        ]

        widgets = {

            'name': forms.TextInput(
                attrs={
                    'class':'form-control'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'rows':4
                }
            )
        }

    def clean_name(self):

        name = self.cleaned_data['name']

        if len(name) < 2:
            raise forms.ValidationError(
                'Skill must be at least 2 characters'
            )

        return name

    def clean_description(self):

        description = self.cleaned_data['description']

        if len(description) < 10:
            raise forms.ValidationError(
                'Skill description must be at least 10 characters'
            )

        return description