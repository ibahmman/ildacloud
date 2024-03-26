from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAdminUser, IsAuthenticated
from .serializers import ProductSerializer, ServiceSerializer


class ProductsAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductSerializer
    # model = serializer_class.Meta.model
    queryset = serializer_class.Meta.model.objects.all()


class ProductsGetAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductSerializer
    queryset = serializer_class.Meta.model.objects.all()


class ServicesAPIView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ServiceSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ServicesGetAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ServiceSerializer
    # model = serializer_class.Meta.model
    queryset = serializer_class.Meta.model.objects.all()
