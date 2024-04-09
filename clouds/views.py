from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.status import (HTTP_100_CONTINUE, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                                   HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS, IsAdminUser
from .serializers import CloudSerializer, ProductCloudSerializer
from services.models import Service, PCloud, Product
from .cpanel import HZCloud
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


class CloudsAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CloudSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        product_cloud
        product_main
        period
        user
        """
        try:
            assert 'product_cloud' in request.data, 'product_cloud is required.'
            assert 'period' in request.data, 'period is required.'
            assert 'image' in request.data, 'image (os name or id) is required.'
            assert 'server_type' in request.data, 'server_type is required.'

            product_cloud = get_object_or_404(PCloud, id=request.data['product_cloud'])
            product_main = get_object_or_404(Product, id=product_cloud.id)
        except AssertionError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'product cloud or product main not found.'}, status=HTTP_404_NOT_FOUND)

        else:
            try:
                can_create = (
                        (self.request.data['period'] == 'hourly' and self.request.user.wallet.having_enough_usdt(
                            product_cloud.price_amount / 30 / 24)) or
                        (self.request.data['period'] == 'daily' and self.request.user.wallet.having_enough_usdt(
                            product_cloud.price_amount / 30)) or
                        (self.request.data['period'] == 'monthly' and self.request.user.wallet.having_enough_usdt(
                            product_cloud.price_amount))
                )
                assert can_create, 'your balance is insufficient.'
                new_cloud = self.model(user=self.request.user, product_main=product_main,
                                       period=self.request.data['period'], product_cloud=product_cloud)
                new_cloud.save()
                new_cloud.last_pay_update()
            except AssertionError as e:
                return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': 'can not create cloud.'}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                if can_create:
                    data = {
                        'image': request.data['image'],
                        'server_type': request.data['server_type'],
                        'name': f'ilda{new_cloud.id}'
                    }

                    if 'datacenter' in request.data: data['datacenter'] = request.data['datacenter']
                    if 'location' in request.data: data['location'] = request.data['location']

                    response = new_cloud.deliver(**data)
                    return Response(response)

        return Response({'hello': 'world.'})


class CloudGetAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CloudSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        print('update')
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print('delete')
        return super().delete(request, *args, **kwargs)


class CloudActionAPIView(APIView):
    """
    :param {
        cloud: x,           # cloud service id
        action: x,          # (0= Stop, 1= Start, 2= Rebuild, 3= Repass, 4= IPv4, 5= IPv6, 6= PTR4)
        more:x,             # (os name, hostname)
    }
    :return CloudService
    """
    permission_classes = (IsAuthenticated, )    # IsOwnerOrAdminUser
    serializer_class = CloudSerializer 
    model = serializer_class.Meta.model
    # model_service = Service

    ACTIONS = ['stop', 'shutdown', 'start', 'reboot', 'restart', 'rebuild', 'passwd',
               'ipv4', 'ipv6', 'ptr4', 'console']   # , 'create', 'delete', 'update'
    OS_LIST = ['w12', 'w19', 'w22', 'u18', 'u20', 'u22', 'd11', 'd10', 'c09', 'c08']

    def post(self, request):
        cloudservice_id = request.data['cloud']
        action = request.data['action']
        more = str(request.data['more']).lower() if 'more' in request.data else 'ildacloud.chelseru.com'

        try:
            cloud = self.model.objects.get(id=cloudservice_id)
            # service = self.model_service.objects.get(id=cloud.id)
            assert isinstance(action, int), 'action should be int.'
            assert action in range(14), 'invalid action. between 0-13'
            if action == 5:
                # rebuild
                assert more in self.OS_LIST, 'invalid os name or id.'
            
        except AssertionError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)
        except:
            return Response({'error': 'cloud service not found.'}, status=HTTP_404_NOT_FOUND)

        else:
            match action:
                case 0:
                    # stop
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 1:
                    # shutdown
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 2:
                    # start
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 3:
                    # reboot
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 4:
                    # restart
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 5:
                    # rebuild
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 6:
                    # passwd
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 7:
                    # ipv4
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 8:
                    # ipv6
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 9:
                    # ptr4
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                case 10:
                    # console
                    if cloud.product_cloud.datacenter.tag == 'HZ':
                        pass
                    pass
                # case 11:
                #     # create
                #     # check wallet if have more than 7 days create.
                #     if self.model.period == 'hourly' and self.request.user.wallet.having_enough_usdt(
                #             self.model.product_cloud.price_amount/30/24):
                #         if cloud.product_cloud.datacenter.tag == 'HZ':
                #             hzcloud = HZCloud.create_a_server()
                #             pass
                #         pass
                #
                #
                #     pass
                # case 12:
                #     # delete
                #     if cloud.product_cloud.datacenter.tag == 'HZ':
                #         pass
                #     pass
                # case 13:
                #     # update
                #     if cloud.product_cloud.datacenter.tag == 'HZ':
                #         pass
                #     pass





