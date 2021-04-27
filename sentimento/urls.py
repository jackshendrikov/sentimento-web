import os

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

# Up two folders to serve "site" content
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('admin/', admin.site.urls),

    # Sample applications
    path('', TemplateView.as_view(template_name='home/main.html'), name='home_page'),
    path('authz/', include('authz.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
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
