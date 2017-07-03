from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.urlpatterns import format_suffix_patterns
# from upload import views
from rest_framework import routers
from upload.views import GenreViewSet, FileViewSet
router = routers.DefaultRouter()
router.register(r'genre', GenreViewSet)
router.register(r'track', FileViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('login.urls')),
    url(r'^app/folders/', include('upload.urls')),
    url(r'^all/', include(router.urls)),
    # url(r'^track/', include(router.urls)),
]

# urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
