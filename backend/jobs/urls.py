from django.urls import path
from .views import (
    JobListCreateView,
    JobDetailView,
    ApplyToJobView,
    EmployerApplicationListView,
)

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list-create'),                      # GET, POST /api/jobs/
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),                      # GET, PUT, DELETE /api/jobs/1/
    path('<int:pk>/apply/', ApplyToJobView.as_view(), name='apply-job'),                # POST /api/jobs/1/apply/
    path('employer/applications/', EmployerApplicationListView.as_view(), name='employer-applications'),
]
