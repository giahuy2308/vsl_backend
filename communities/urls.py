from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import *

route = SimpleRouter()
route.register(f"communities", CommunityView)
route.register(f"community/rule", CommunityRuleView)
route.register(f"community/joininrequest", JoinInRequestView)
route.register(f"community/participant", ParticipantView)
route.register(f"community/reaction", ReactionView)
route.register(f"community/post", PostView)
route.register(f"community/comment", CommentView)


urlpatterns = route.urls
