from django.urls import path
from .views import UserLogin, ProfileCreate, ProfileView, UpdateUser, UpdateProfile, UpdateEmail, VerifyEmail, RecoveryEmail, SMSAuth, UpdateMobile

app_name = '_profiles'
urlpatterns = [
    # details.
    path('', ProfileView.as_view(), name='index'),
    path('q/mobile/', SMSAuth.as_view(), name='sms-auth'),
    path('q/signup/', ProfileCreate.as_view(), name='signup'),
    path('q/login/', UserLogin.as_view(), name='login'),

    # updates.
    path('u/user/<str:username>/', UpdateUser.as_view(), name='update-user'),
    path('u/profile/<str:username>/', UpdateProfile.as_view(), name='update-profile'),
    path('u/email/<str:username>/', UpdateEmail.as_view(), name='update-email'),
    # ------------------------------------------------------------------
    path('u/mobile/<str:username>/', UpdateMobile.as_view(), name='update-mobile'),

    
    #   ----- emails changing urls. -----
    path('v/<slug:token>/', VerifyEmail.as_view(), name='verify-email'),
    path('r/<slug:token>/', RecoveryEmail.as_view(), name='recovery-email'),

]