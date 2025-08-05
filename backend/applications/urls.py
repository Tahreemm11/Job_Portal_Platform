from django.urls import path
from .views import (
    JobApplicationCreateView,
    EmployerApplicationList,
    ApplicationStatusUpdate,
    ViewResumeFile
)

urlpatterns = [
    path('', JobApplicationCreateView.as_view(), name='apply-job'),
    path('employer/applications/', EmployerApplicationList.as_view(), name='employer-applications'),
    path('application/<int:pk>/status/', ApplicationStatusUpdate.as_view(), name='update-application-status'),
    path('application/<int:pk>/resume/', ViewResumeFile.as_view(), name='view-resume'),
]
