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


class PageView(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReactionView(viewsets.ModelViewSet):
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        try:
            return Reaction.objects.get(pk=pk)
        except Reaction.DoesNotExist:
            raise Http404

    def perform_create(self, serializer, content_type_id, obj_pk):
        serializer.save(content_type=content_type_id, object_id=obj_pk, author=self.request.user)

    def create(self, request, content_type_id, obj_pk):
        serializer = ReactionSerializer(data=request.data)

        contenttype = ContentType.objects.get(id=content_type_id)

        if contenttype.name in ["page","comment"]:
            if contenttype.name == "page" and len(Page.objects.filter(id=obj_pk)) == 0:
                return Response({"detail":"Not Found"}, status=status.HTTP_404_NOT_FOUND)
            if contenttype.name == "comment" and len(Comment.objects.filter(id=obj_pk)) == 0:
                return Response({"detail":"Not Found"},status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail":"Not Found"},status=status.HTTP_404_NOT_FOUND)
        

        if serializer.is_valid():
            self.perform_create(serializer=serializer, content_type_id=contenttype, obj_pk=obj_pk)
            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    def update(self, request, content_type_id, obj_pk, pk):
        reaction = self.get_object(pk=pk)
        serializer = ReactionSerializer(reaction,data=request.data)

        contenttype = ContentType.objects.get(id=content_type_id)

        if serializer.is_valid():
            self.perform_create(serializer=serializer, content_type_id=contenttype, obj_pk=obj_pk)
            return Response(serializer.data,status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        


