from rest_framework import routers
from rest_framework.routers import SimpleRouter
from .views import *

route = SimpleRouter()
route.register(f"",CommunityView )
route.register(f"reactions",ReactionView )
route.register(f"pages",PageView )
route.register(f"comments",CommentView)


urlpatterns = route.urls