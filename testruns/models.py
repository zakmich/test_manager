from django.db import models
from django.contrib.auth.models import User
from testcases.models import Project, TestCase # Importujemy modele z sąsiedniej apki

class TestRun(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200, help_text="Np. Release 1.0 Regression")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

class TestExecution(models.Model):
    STATUS_CHOICES = [
        ('unt', 'Untested'),
        ('pass', 'Passed'),
        ('fail', 'Failed'),
        ('blck', 'Blocked'),
    ]

    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name='executions')
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='unt')
    comment = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test_run.name} | {self.test_case.title}: {self.status}"
