from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from rest_framework.views import Response, status
from rest_framework import viewsets

from .serializers import *
from .models import * 

# Create your views here.

class CommunityView(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def perform_create(self, serializer):
        serializer.save(administrator=self.request.user)

class PageView(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionView(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            raise Http404
        
    def get_content_type(self, content_type):
        try:
            return ContentType.objects.get(model=content_type)
        except ContentType.DoesNotExist:
            raise Http404

    def perform_create(self, serializer, content_type, obj_pk):
        serializer.save(content_type=content_type, object_id=obj_pk, author=self.request.user)

    def list(self, request, content_type, obj_pk):
        contenttype = self.get_content_type(content_type=content_type)
        reaction = Reaction.objects.filter(content_type=contenttype, object_id=obj_pk, author=request.user)
        serializer = ReactionSerializer(reaction, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, content_type, obj_pk):
        contenttype = self.get_content_type(content_type=content_type)
        serializer = ReactionSerializer(data=request.data)
        reaction = Reaction.objects.filter(content_type=contenttype, object_id=obj_pk)

        def get_value():
            if contenttype.name == "page":
                return len(Page.objects.filter(pk=obj_pk)) != len(reaction.filter(author=request.user))
            else:
                return len(Comment.objects.filter(pk=obj_pk)) != len(reaction.filter(author=request.user))

        if serializer.is_valid() and get_value():
            self.perform_create(serializer=serializer, content_type=contenttype, obj_pk=obj_pk)
            return Response({"status":"Bày tỏ cảm xúc thành công"},status=status.HTTP_200_OK)

        return Response({"status":"Bày tỏ cảm xúc không thành công"},status=status.HTTP_400_BAD_REQUEST)
    
