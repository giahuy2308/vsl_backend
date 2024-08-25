from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.db.models import Q

from vsl.permissions import IsSuperUserOrReadOnly, IsAuthor
from django.conf import settings
from .serializers import NotificationSerializer, CustomUserSerializer
from .models import Notification

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView # type: ignore
from rest_framework.views import APIView, Response, status
from rest_framework.decorators import action
from rest_framework import viewsets, permissions

from djoser.social.views import ProviderAuthView

class CustomProviderAuthView(ProviderAuthView):
    def post(self,request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")
            response["Content-Type"] = 'application/x-www-form-urlencoded'
            
            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
            
            response.set_cookie(
                "refresh",
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
        

        return response


class NotificationView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsSuperUserOrReadOnly, IsAuthor]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_content_type(self, content_type):
        try:
            return ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise Http404

    def get_queryset(self):
        From = self.request.GET.get("From")
        object_id = self.request.GET.get("obj_pk")
        query = self.request.GET.get("q")
        
        if From is not None and query is not None:
            contenttype = self.get_content_type(From)
            if object_id is not None:
                self.queryset = Notification.objects.filter(Q(content__icontains=query), From=contenttype, object_id=object_id)
            else:
                self.queryset = Notification.objects.filter(Q(content__icontains=query), From=contenttype)
        else:
            if From is not None:
                contenttype = self.get_content_type(From)
                if object_id is not None:
                    self.queryset = Notification.objects.filter(From=contenttype, object_id=object_id)
                else:
                    self.queryset = Notification.objects.filter(From=contenttype)
            if query is not None:
                self.queryset = Notification.objects.filter(Q(content__icontains=query)) 

        return super().get_queryset()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")
            refresh_token = response.data.get("refresh")

            response.set_cookie(
                "access",
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
            
            response.set_cookie(
                "refresh",
                refresh_token,
                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")

        data = request.data.copy()

        if refresh_token:
            data["refresh"] = refresh_token

        request._full_data = data

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get("access")

            response.set_cookie(
                key="access",
                value=access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
        return response
    

class CustomTokenVerifyView(TokenVerifyView):
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get("access")
        if access_token:
            request.data['token'] = access_token
            
        return super().post(request, *args, **kwargs)


class LogOutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")

        return response