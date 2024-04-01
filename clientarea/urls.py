from django.urls import path
from .views import AccountUserCreateStandardAPIView

app_name = 'clientarea'
urlpatterns = [
    path('register-standard/', AccountUserCreateStandardAPIView.as_view(), name='apiv1-account-create-standard')
]
