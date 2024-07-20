from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *

route = SimpleRouter()
route.register(f"communities",CommunityView )
route.register(f"community/reactions",ReactionView )
route.register(f"community/pages",PageView )
route.register(f"community/comments",CommentView)


urlpatterns = [
    path("community/reactions/<str:content_type>/<int:obj_pk>/", ReactionView.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path("community/reactions/<int:pk>/", ReactionView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
        
    }))
] + route.urls