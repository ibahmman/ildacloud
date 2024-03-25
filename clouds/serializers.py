from rest_framework.serializers import Serializer, ModelSerializer
from services.models import SCloud, PCloud


class ProductCloudSerializer(ModelSerializer):
    class Meta:
        model = PCloud
        fields = '__all__'
        depth = 2


class CloudSerializer(ModelSerializer):
    class Meta:
        model = SCloud
        fields = '__all__'
        depth = 2

