from django.urls import path
from .views import CloudsAPIView, CloudGetAPIView

app_name = 'clouds'
urlpatterns = [
    path('list/', CloudsAPIView.as_view(), name='apiv1-clouds-list'),
    path('get/<str:pk>/', CloudGetAPIView.as_view(), name='apiv1-cloud-get'),
]
