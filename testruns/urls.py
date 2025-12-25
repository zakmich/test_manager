from django.urls import path
from .views import TestRunDetailView, change_execution_status, TestRunCreateView, TestRunListView, close_testrun, \
    fail_with_comment, block_with_comment

urlpatterns = [
    path('', TestRunListView.as_view(), name='testrun_list'),
    path('new/', TestRunCreateView.as_view(), name='testrun_new'),
    path('<int:pk>/', TestRunDetailView.as_view(), name='run_detail'),
    path('execution/<int:pk>/status/<str:new_status>/', change_execution_status, name='change_status'),
    path('<int:pk>/close/', close_testrun, name='close_testrun'),
    path('execution/<int:pk>/fail-comment/', fail_with_comment, name='fail_with_comment'),
    path('execution/<int:pk>/block-comment/', block_with_comment, name='block_with_comment'),
]
