from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('HOME.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('mgc/',include('MGC.urls')),
]
