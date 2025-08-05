from django.contrib import admin
from .models import User, EmployerProfile, JobSeekerProfile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email']

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'company_name', 'website']
    search_fields = ['company_name', 'user__username']

@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    search_fields = ['user__username']
