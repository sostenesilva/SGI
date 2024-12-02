from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('HOME.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('gestaocontratos/',include('MGC.urls')),
    path('combustiveis/',include('MGCOMBUSTIVEIS.urls')),
    path('regularidadefiscal/',include('MGREGULARIDADEFISCAL.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
