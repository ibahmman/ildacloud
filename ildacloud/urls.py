from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my/', include('accounts.urls')),
    path('financial/', include('financial.urls')),
    path('services/', include('services.urls')),
    path('', include('store.urls')),
]
