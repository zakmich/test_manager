from django.views.generic import TemplateView
from django.db.models import Count, Q
from testruns.models import TestRun
from testcases.models import Tag, Project  # Opcjonalnie, jeśli chcesz wyświetlać tagi


class DashboardView(TemplateView):  # Dodałem TemplateView zamiast LoginRequiredMixin dla ułatwienia testów
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 1. KPI: Aktywne Runy z obliczeniami
        active_runs = TestRun.objects.filter(status='active').annotate(
            total_tests=Count('executions'),
            passed=Count('executions', filter=Q(executions__status='pass')),
            failed=Count('executions', filter=Q(executions__status='fail')),
            blocked=Count('executions', filter=Q(executions__status='blck')),
        ).order_by('-created_at')[:5]

        # Prosta logika obliczania procentów dla paska postępu
        for run in active_runs:
            if run.total_tests > 0:
                run.progress_percent = int(((run.passed + run.failed + run.blocked) / run.total_tests) * 100)
            else:
                run.progress_percent = 0

        context['active_runs'] = active_runs

        # 2. Popularne tagi (prosty przykład)

        projects = Project.objects.annotate(
            case_count=Count('testcase')
        ).order_by('-created_at')

        context['projects'] = projects  # Przekazujemy do szablonu

        # 3. Tagi (to już masz)
        context['tags'] = Tag.objects.all()[:10]

        return context


