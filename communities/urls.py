from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *

route = SimpleRouter()
route.register(f"communities",CommunityView )
route.register(f"community/reaction",ReactionView )
route.register(f"community/page",PageView )
route.register(f"community/comment",CommentView)


urlpatterns = route.urls