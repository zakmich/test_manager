from django import forms
from .models import TestRun


class TestRunForm(forms.ModelForm):
    class Meta:
        model = TestRun
        fields = ['name', 'project']  # Użytkownik podaje tylko nazwę i projekt

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'np. Regresja v1.0'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Nazwa Test Runu',
            'project': 'Wybierz Projekt',
        }
