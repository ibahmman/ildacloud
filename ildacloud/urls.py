from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('my/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('clouds/', include('clouds.urls')),
    path('', include('storearea.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
