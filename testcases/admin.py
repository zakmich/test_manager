from django.contrib import admin
from .models import Project, TestCase, Tag

admin.site.register(Project)
admin.site.register(TestCase)
admin.site.register(Tag)
