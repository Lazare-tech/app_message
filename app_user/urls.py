from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
import app_user.views
###
app_name = "app_user"

urlpatterns = [
    path('', app_user.views.home, name='homepage'),
      

 
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)