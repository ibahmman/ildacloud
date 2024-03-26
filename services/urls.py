from django.urls import path
from .views import ProductsAPIView, ServicesAPIView, ProductsGetAPIView, ServicesGetAPIView


app_name = 'services'
urlpatterns = [
    path('products/', ProductsAPIView.as_view(), name='apiv1-products-list-create'),
    path('products-get/<str:pk>/', ProductsGetAPIView.as_view(), name='apiv1-products-get'),
    path('list/', ServicesAPIView.as_view(), name='apiv1-services-list'),
    path('get/<str:pk>/', ServicesGetAPIView.as_view(), name='apiv1-services-get'),
]
