from rest_framework.serializers import Serializer, ModelSerializer
from services.models import SCloud as Service


class CloudSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        depth = 2

