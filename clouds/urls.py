from django.urls import path
from .views import CloudsAPIView, CloudGetAPIView, CloudProductsAPIView

app_name = 'clouds'
urlpatterns = [
    path('products/', CloudProductsAPIView.as_view(), name='apiv1-clouds-products'),
    path('list/', CloudsAPIView.as_view(), name='apiv1-clouds-list'),
    path('get/<str:pk>/', CloudGetAPIView.as_view(), name='apiv1-cloud-get'),
]
