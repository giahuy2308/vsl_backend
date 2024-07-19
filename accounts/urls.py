from django.urls import path
from .views import SignUpView, LogInView, LogOutView, NotificationView
from rest_framework.routers import SimpleRouter

route = SimpleRouter()
route.register(f"notifications", NotificationView)


urlpatterns =  [ 
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
] + route.urls