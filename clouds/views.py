from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS, IsAdminUser
from .serializers import CloudSerializer, ProductCloudSerializer


class CloudProductsAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductCloudSerializer
    # model = serializer_class.Meta.model
    queryset = serializer_class.Meta.model.objects.all()


class CloudProductsGetAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductCloudSerializer
    queryset = serializer_class.Meta.model.objects.all()


class CloudsAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CloudSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class CloudGetAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CloudSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

