from django.urls import path, re_path

from rest_framework.routers import SimpleRouter, DefaultRouter

from .views import *

from djoser.urls.base import router, views 

router = DefaultRouter()
router.register(f"notification", NotificationView, basename="not")
router.register(f"", views.UserViewSet, basename="user")

urlpatterns =  [ 
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name="provider-auth"
    ),
    path('logout/', LogOutView.as_view(), name='logout'),
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", CustomTokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", CustomTokenVerifyView.as_view(), name="jwt-verify"),
    
] + router.urls