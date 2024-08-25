from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('lessons.urls')),
    path('', include('communities.urls')),
    # 3rd-party
    # path(r'^auth/', include('djoser.social.urls')),
    path('', include('social_django.urls', namespace='social')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])