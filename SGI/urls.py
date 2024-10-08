from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('mgc/',include('MGC.urls')),
] + static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0]) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
