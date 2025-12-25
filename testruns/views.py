from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import TestRun, TestExecution
from testcases.models import TestCase
from .forms import TestRunForm

class TestRunListView(ListView):
    model = TestRun
    template_name = 'testruns/testrun_list.html'
    context_object_name = 'testruns'
    ordering = ['-created_at']

class TestRunDetailView(DetailView):
    model = TestRun
    template_name = "testruns/run_detail.html"
    context_object_name = "run"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pobieramy wszystkie wykonania dla tego runu
        context['executions'] = self.object.executions.select_related('test_case').all()
        return context

@require_POST  # Zabezpieczenie: ta funkcja zadziała tylko przy wysłaniu formularza
def change_execution_status(request, pk, new_status):
    # 1. Pobierz konkretne wykonanie testu (lub zwróć błąd 404 jeśli nie istnieje)
    execution = get_object_or_404(TestExecution, pk=pk)

    # 2. Zmień status (tylko jeśli jest poprawny)
    valid_statuses = ['pass', 'fail', 'blck', 'unt']
    if new_status in valid_statuses:
        execution.status = new_status
        execution.save()

    # 3. Wróć do strony szczegółów runu
    return redirect('run_detail', pk=execution.test_run.id)


class TestRunCreateView(CreateView):
    model = TestRun
    form_class = TestRunForm
    template_name = 'testruns/testrun_form.html'

    # Po utworzeniu przekieruj od razu do szczegółów tego nowego runu (żeby zacząć testować)
    def get_success_url(self):
        return reverse_lazy('run_detail', kwargs={'pk': self.object.pk})

    def get_initial(self):
        initial = super().get_initial()
        # Sprawdzamy, czy w adresie URL jest parametr 'project_id'
        project_id = self.request.GET.get('project_id')
        if project_id:
            # Jeśli jest, ustawiamy początkową wartość pola 'project' w formularzu
            initial['project'] = project_id
        return initial

    def form_valid(self, form):
        # 1. Najpierw standardowo zapisz TestRun w bazie
        response = super().form_valid(form)

        # 2. "self.object" to teraz nasz nowo utworzony TestRun.
        # Pobierz projekt, który wybrał użytkownik
        selected_project = self.object.project

        # 3. Znajdź wszystkie testy należące do tego projektu
        tests_in_project = TestCase.objects.filter(project=selected_project)

        # 4. Utwórz TestExecution dla każdego znalezionego testu
        executions_to_create = []
        for test_case in tests_in_project:
            executions_to_create.append(
                TestExecution(
                    test_run=self.object,
                    test_case=test_case,
                    status='unt'  # Domyślnie Untested
                )
            )

        # Bulk create jest szybsze niż zapisywanie w pętli pojedynczo
        TestExecution.objects.bulk_create(executions_to_create)

        return response

@require_POST
def close_testrun(request, pk):
    """Zamyka test run, zmieniając status na 'completed'"""
    run = get_object_or_404(TestRun, pk=pk)
    run.status = 'completed'
    run.save()
    return redirect('testrun_list')


@require_POST
def fail_with_comment(request, pk):
    """Zmienia status na FAIL i zapisuje komentarz"""
    execution = get_object_or_404(TestExecution, pk=pk)
    comment = request.POST.get('comment', '').strip()

    # 1. ZAPISZ KOMENTARZ
    execution.comment = comment

    # 2. ZMIEŃ STATUS NA FAIL
    execution.status = 'fail'

    execution.save()

    base_url = reverse('run_detail', args=[execution.test_run.id])
    return redirect(f"{base_url}?expanded={execution.id}")


@require_POST
def block_with_comment(request, pk):
    """Zmienia status na BLOCKED i zapisuje komentarz"""
    execution = get_object_or_404(TestExecution, pk=pk)
    comment = request.POST.get('comment', '').strip()

    # 1. ZAPISZ KOMENTARZ
    execution.comment = comment

    # 2. ZMIEŃ STATUS NA BLOCKED
    execution.status = 'blck'

    execution.save()

    base_url = reverse('run_detail', args=[execution.test_run.id])
    return redirect(f"{base_url}?expanded={execution.id}")
