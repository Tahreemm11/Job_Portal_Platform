from rest_framework import serializers
from .models import Job
from applications.models import Application
from users.serializers import UserSerializer, RegisterSerializer

# ✅ Serializer for Job model
class JobSerializer(serializers.ModelSerializer):
    employer = UserSerializer(read_only=True)  # Show nested employer info (username, email, etc.)

    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['employer', 'posted_at']  # These are auto-handled

# ✅ Serializer for Application model
class ApplicationSerializer(serializers.ModelSerializer):
    applicant = RegisterSerializer(read_only=True)  # Show nested user info

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['applicant', 'resume', 'applied_at']
