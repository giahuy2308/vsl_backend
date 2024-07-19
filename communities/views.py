from rest_framework import viewsets
from .models import * 
from .serializers import *

# Create your views here.

class CommunityView(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class ReactionView(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer


class PageView(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer