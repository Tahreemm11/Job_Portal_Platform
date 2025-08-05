from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import JobSeekerProfile, EmployerProfile
from .serializers import (
    RegisterSerializer,
    JobSeekerProfileSerializer,
    EmployerProfileSerializer,
    UserSerializer
)
from .token_serializers import MyTokenObtainPairSerializer


## ✅ Registration with token return
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # ✅ Proper password hashing
            user.is_active = True  # ✅ Ensure active
            user.save()

            role = serializer.validated_data.get('role')

            # Create appropriate profile
            if role == 'job_seeker':
                JobSeekerProfile.objects.create(user=user)
            elif role == 'employer':
                EmployerProfile.objects.create(user=user)

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ JWT Login View
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# ✅ User Profile View & Update
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_data = {}

        if user.role == 'job_seeker':
            profile = getattr(user, 'jobseeker_profile', None)
            profile_data = JobSeekerProfileSerializer(profile).data if profile else {}

        elif user.role == 'employer':
            profile = getattr(user, 'employer_profile', None)
            profile_data = EmployerProfileSerializer(profile).data if profile else {}

        return Response({
            "user": UserSerializer(user).data,
            "profile": profile_data
        })

    def patch(self, request):
        user = request.user

        if user.role == 'job_seeker':
            profile = getattr(user, 'jobseeker_profile', None)
            serializer = JobSeekerProfileSerializer(profile, data=request.data, partial=True)

        elif user.role == 'employer':
            profile = getattr(user, 'employer_profile', None)
            serializer = EmployerProfileSerializer(profile, data=request.data, partial=True)

        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
