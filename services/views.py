from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from .serializers import ProductSerializer, ServiceSerializer


class ProductsAPIView(ListCreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ProductSerializer
    # model = serializer_class.Meta.model
    queryset = serializer_class.Meta.model.objects.all()


class ServicesAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ServiceSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
