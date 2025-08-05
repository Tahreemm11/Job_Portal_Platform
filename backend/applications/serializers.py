from rest_framework import serializers
from .models import Application
from users.serializers import UserSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    resume = serializers.FileField(required=True)  # ✅ Allow resume upload

    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['user', 'applied_at']  # ✅ 'resume' removed from here
