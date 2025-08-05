from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'employer', 'location', 'salary_min', 'salary_max', 'posted_at']
    ordering = ['-posted_at']
    search_fields = ['title', 'location']
    list_filter = ['location']
