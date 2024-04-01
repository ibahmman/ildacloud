from django.urls import path, include
from .views import ProfilesAPIView, ProfileCreateAPIView

app_name = 'accounts'
urlpatterns = [
    path('profiles/', ProfilesAPIView.as_view(), name='apiv1-profiles-list'),
    # path('register-standard/', ProfileCreateAPIView.as_view(), name='apiv1-profiles-create-standard'),
    # path('register-mobile/', )
]
