from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import CloudSerializer


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

