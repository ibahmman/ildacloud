from django.urls import path
from .views import CloudsList, CloudDetail

app_name = 'clouds'

urlpatterns = [
    path('', CloudsList.as_view(), name='clouds-list'),
    path('<str:pk>/', CloudDetail.as_view(), name='cloud-detail'),
]
