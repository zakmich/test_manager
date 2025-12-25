from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView, DetailView
from .models import TestCase, Project
from .forms import TestCaseForm, ProjectForm


class TestCaseUpdateView(UpdateView):
    model = TestCase
    form_class = TestCaseForm
    template_name = 'testcases/testcase_form.html'

    def get_success_url(self):
        # 1. Sprawdź czy w URL jest parametr ?next=/runs/5/
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        # 2. Jeśli nie ma, wróć do domyślnej listy
        return reverse_lazy('testcase_list')


# 1. Widok Listy (Repozytorium)
class TestCaseListView(ListView):
    model = TestCase
    template_name = 'testcases/testcase_list.html'
    context_object_name = 'testcases'
    ordering = ['-created_at']  # Najnowsze na górze


# 2. Widok Tworzenia (Nowy test)
class TestCaseCreateView(CreateView):
    model = TestCase
    form_class = TestCaseForm
    template_name = 'testcases/testcase_form.html'  # Używamy tego samego szablonu co przy edycji!
    success_url = reverse_lazy('testcase_list')  # Po sukcesie wróć do listy

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False  # Mówimy szablonowi: "To jest nowy element"
        return context

    def get_initial(self):
        initial = super().get_initial()
        project_id = self.request.GET.get('project_id')
        if project_id:
            initial['project'] = project_id
        return initial

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'testcases/project_form.html'
    success_url = reverse_lazy('home') # Po utworzeniu wracamy na Dashboard

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'testcases/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobieramy testy przypisane tylko do tego projektu
        # Order_by('-created_at') sprawi, że najnowsze będą na górze
        context['testcases'] = TestCase.objects.filter(project=self.object).order_by('-created_at')
        return context

class ProjectListView(ListView):
    model = Project
    template_name = 'testcases/project_list.html'
    context_object_name = 'projects'
    ordering = ['-created_at']