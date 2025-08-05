from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.serializers import UserSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)

        data['refresh'] = str(token)
        data['access'] = str(token.access_token)
        data['user'] = UserSerializer(self.user).data

        return data
