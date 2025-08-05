from rest_framework import serializers
from .models import User, JobSeekerProfile, EmployerProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'role',
            'full_name', 'phone_number', 'profile_picture'
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            full_name=validated_data.get('full_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            profile_picture=validated_data.get('profile_picture', None),
        )
        return user

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = ['skills', 'resume']

class EmployerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_logo', 'website']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
