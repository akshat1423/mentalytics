from django.contrib import admin
from django.urls import path, include
from django.urls.conf import include
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aiapp.urls')),  # Include the chat app URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
