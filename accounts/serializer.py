from rest_framework.serializers import Serializer, ModelSerializer
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'is_active')

class ProfileSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = '__all__'
        # depth = 2
    
    


