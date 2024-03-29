from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND)
from .serializer import ProfileSerializer


class ProfileCreateAPIView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ProfileSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def perform_create(self, serializer):
        print(serializer.data)
        # create user first
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class ProfilesAPIView(ListAPIView):
    permission_classes = (IsAdminUser, )
    serializer_class = ProfileSerializer
    queryset = serializer_class.Meta.model.objects.all()
