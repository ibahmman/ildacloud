from rest_framework.serializers import Serializer, ModelSerializer
from .models import Profile


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 2

