from rest_framework.serializers import Serializer, ModelSerializer
from .models import Product, Service


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        depth = 2


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        depth = 2
