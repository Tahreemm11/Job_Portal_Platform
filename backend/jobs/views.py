from rest_framework import generics, permissions, filters, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404

from .models import Job
from .serializers import JobSerializer, ApplicationSerializer
from applications.models import Application
from users.models import JobSeekerProfile
from users.serializers import RegisterSerializer

# ✅ (Optional) Register from here (if needed separately)
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            user.is_active = True
            user.save()
            return Response({"user": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ POST/LIST JOBS
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all().order_by('-posted_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description', 'location']

    def perform_create(self, serializer):
        if self.request.user.role != 'employer':
            raise PermissionDenied("Only employers can post jobs.")
        serializer.save(employer=self.request.user)


# ✅ JOB DETAIL, UPDATE, DELETE
class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        job = self.get_object()
        if job.employer != self.request.user:
            raise PermissionDenied("You can only update your own job.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.employer != self.request.user:
            raise PermissionDenied("You can only delete your own job.")
        instance.delete()


# ✅ APPLY TO JOB
class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'job_seeker':
            raise ValidationError("Only job seekers can apply.")

        profile = get_object_or_404(JobSeekerProfile, user=user)
        job = get_object_or_404(Job, id=self.kwargs['pk'])

        if Application.objects.filter(job=job, applicant=user).exists():
            raise ValidationError("You have already applied to this job.")

        serializer.save(
            job=job,
            applicant=user,
            resume=profile.resume
        )


# ✅ VIEW APPLICATIONS RECEIVED BY EMPLOYER
class EmployerApplicationListView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'employer':
            raise PermissionDenied("Only employers can view this.")
        return Application.objects.filter(job__employer=user).order_by('-applied_at')
