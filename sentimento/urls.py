import os

from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

# Up two folders to serve "site" content
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sample applications
    path('', include('home.urls')),
    path('authz/', include('authz.urls')),
    path('analyzer/', include('analyzer.urls', namespace='analyzer')),
]

# Serve the favicon
urlpatterns += [
    path('favicon.ico', serve, {
        'path': 'favicon.ico',
        'document_root': os.path.join(BASE_DIR, 'home/static'),
    }),
]

# Serve the media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
