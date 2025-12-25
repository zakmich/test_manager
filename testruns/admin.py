from django.contrib import admin
from .models import TestRun, TestExecution

admin.site.register(TestRun)
admin.site.register(TestExecution)
