from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.status import HTTP_100_CONTINUE, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS, IsAdminUser
from .serializers import CloudSerializer, ProductCloudSerializer
from services.models import Service
from time import sleep


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


class CloudActionAPIView(APIView):
    """
    :param {
        cloud: x,           # cloud service id
        action: x,          # (0= Stop, 1= Start, 2= Rebuild, 3= Repass, 4= IPv4, 5= IPv6, 6= PTR4)
        more:x,             # (os name, hostname)
    }
    :return CloudService
    """
    permission_classes = (IsAuthenticated, ) # IsOwnerOrAdminUser
    serializer_class = CloudSerializer 
    model = serializer_class.Meta.model
    model_service = Service

    ACTIONS = ['stop', 'start', 'reboot', 'rebuild', 'passwd', 'ipv4', 'ipv6', 'ptr4']
    OS_LIST = ['w12', 'w19', 'w22', 'u18', 'u20', 'u22', 'd11', 'd10', 'c09', 'c08']

    def post(self, request):
        cloudservice_id = request.data['cloud']
        action = request.data['action']
        more = str(request.data['more']).lower() if 'more' in request.data else 'ildacloud.chelseru.com'

        try:
            cloud = self.model.objects.get(id=cloudservice_id)
            service = self.model_service.objects.get(id=cloud.id)
            assert isinstance(action, int), 'action should be int.'
            assert action in range(9), 'invalid action. between 0-6'
            if action is 3:
                # rebuild
                assert more in self.OS_LIST, 'invalid os name.'
            
        except AssertionError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'cloud service not found.'}, status=HTTP_404_NOT_FOUND)

        else:
            sleep(2)
            match action:
                case 0:
                    # stop
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 1:
                    # start
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 2:
                    # reboot
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 3:
                    # rebuild
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 4:
                    # passwd
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 5:
                    # ipv4
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 6:
                    # ipv6
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 7:
                    # ptr4
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass






