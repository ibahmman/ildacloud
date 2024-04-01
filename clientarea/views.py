from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND, HTTP_409_CONFLICT)
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password
from accounts.serializer import ProfileSerializer


class AccountUserCreateStandardAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = ProfileSerializer
    model = serializer_class.Meta.model

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        try:
            # if 'mobile' in request.data:
            #     mobile = request.data['mobile']
            #     if self.model.objects.filter(mobile=mobile) or User.objects.filter(username=mobile):
            #         return Response({'error': 'mobile is already exist. please change your mobile number.'}, status=HTTP_409_CONFLICT)
            # if 'referral' in request.data:
            #     referral = request.data['refferal']
            #     if not User.objects.filter(username=referral):
            #         return Response({'error': 'your referral user is not found. please check it again or remove field.'}, status=HTTP_404_NOT_FOUND)

            if User.objects.filter(username=username):
                return Response({'error': 'username is already exist. please try an other username.'}, status=HTTP_409_CONFLICT)
            
            user = User.objects.create(username=username, password=make_password(password))
            account = self.model(user=user)
            account.save()
            return Response({'message': 'account created.'}, status=HTTP_201_CREATED)
            
        except:
            return Response({'error': 'can not create your account. please contact to support.'}, status=HTTP_400_BAD_REQUEST)
            
