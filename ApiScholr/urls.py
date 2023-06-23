from django.contrib import admin
from django.urls import path,  include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('classes.urls')),
    path('', include('calendrier.urls')),
    path('', include('evals.urls')),
    path('', include('suivi.urls')),
    path('', include('reseau.urls')),
    path('', include('etabs.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
