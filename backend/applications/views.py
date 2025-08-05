from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
import os

from .models import Application
from .serializers import ApplicationSerializer
from jobs.models import Job


# ✅ Job Seeker: Apply to a Job
class JobApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Enable file upload

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ Employer: View all applications for their jobs
class EmployerApplicationList(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(job__employer=self.request.user)


# ✅ Employer: Update Application Status (pending, selected, etc.)
class ApplicationStatusUpdate(generics.UpdateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        application = self.get_object()

        if application.job.employer != request.user:
            return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        new_status = request.data.get('status')
        if new_status not in dict(Application.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        application.save()
        return Response({"success": f"Status updated to '{new_status}'"})


# ✅ Employer: View or Download Resume File
class ViewResumeFile(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)

        # Only employer who owns the job can view
        if application.job.employer != request.user:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        if not application.resume:
            return Response({"error": "No resume found"}, status=status.HTTP_404_NOT_FOUND)

        file_path = os.path.join(settings.MEDIA_ROOT, str(application.resume))
        if not os.path.exists(file_path):
            return Response({"error": "File not found on server"}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
