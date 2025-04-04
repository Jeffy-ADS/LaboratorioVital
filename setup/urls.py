from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
    path('usuarios', include('usuarios.urls')),
    path('exames/', include('exames.urls')),
    path('empresarial/', include('empresarial.urls')),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)