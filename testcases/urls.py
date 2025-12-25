from django.urls import path
from .views import (TestCaseUpdateView, TestCaseListView, TestCaseCreateView, ProjectCreateView, ProjectDetailView,
                    ProjectListView)

urlpatterns = [
    # Lista wszystkich testów
    path('', TestCaseListView.as_view(), name='testcase_list'),

    # Dodawanie nowego
    path('new/', TestCaseCreateView.as_view(), name='testcase_new'),

    # Edycja (to już masz)
    path('edit/<int:pk>/', TestCaseUpdateView.as_view(), name='testcase_edit'),

    path('project/new/', ProjectCreateView.as_view(), name='project_new'),

    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),

    path('projects/', ProjectListView.as_view(), name='project_list'),
]
