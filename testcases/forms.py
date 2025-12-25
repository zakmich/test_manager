from django import forms
from .models import TestCase, Project


class TestCaseForm(forms.ModelForm):
    class Meta:
        model = TestCase
        fields = ['project','title', 'priority', 'description', 'steps', 'expected_result', 'tags']

        # Tu dodajemy klasy Bootstrapa, żeby formularz był ładny
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Wpisz tytuł testu'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'steps': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'expected_result': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'style': 'height: 100px;'}),
        }
        labels = {
            'project': 'Wybierz Projekt',
            'title': 'Tytuł Przypadku',
            'steps': 'Kroki Testowe',
            'expected_result': 'Oczekiwany Rezultat',
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Np. Sklep Internetowy v2'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Krótki opis projektu...'}),
        }
        labels = {
            'name': 'Nazwa Projektu',
            'description': 'Opis',
        }