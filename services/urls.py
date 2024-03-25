from django.urls import path
from .views import ProductsAPIView, ServicesAPIView


app_name = 'services'
urlpatterns = [
    path('products/', ProductsAPIView.as_view(), name='apiv1-products-list-create'),
    path('list/', ServicesAPIView.as_view(), name='apiv1-services-list'),
]
