from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import Http404

from rest_framework.views import Response, status
from rest_framework import viewsets, permissions

from vsl.permissions import IsAuthorOrReadOnly, ParticipantPer
from accounts.models import Notification
from .serializers import *
from .models import * 

# Create your views here.

class CommunityView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly,ParticipantPer]
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None: 
            self.queryset = Community.objects.filter(
                Q(name__icontains=query) | Q(administrator__username__icontains=query)
            )
        return super().get_queryset()

    def perform_create(self, serializer):
        participants = serializer.validated_data.get("participant", [])
        participants += [self.request.user]
        serializer.save(administrator=self.request.user, participant=participants)

class PageView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly,ParticipantPer]
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None: 
            self.queryset = Community.objects.filter(
                Q(content__icontains=query) | Q(author__username__icontains=query) | Q(community__name__icontains=query)
            )
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly,ParticipantPer]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionView(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrReadOnly,ParticipantPer]
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
        

    def get_queryset(self):
        contenttype = self.request.GET.get("contenttype")
        object_id = self.request.GET.get("obj_pk")

        if contenttype is not None:
            contenttype = self.get_content_type(contenttype)
            if object_id is not None:
                self.queryset = Reaction.objects.filter(content_type=contenttype, object_id=object_id)
            else:
                self.queryset = Reaction.objects.filter(content_type=contenttype)

        return super().get_queryset()

    def create(self, request):
        contenttype = self.get_content_type(self.request.GET.get("contenttype"))
        obj_pk=self.request.GET.get("obj_pk")
        serializer = ReactionSerializer(data=request.data)
        reaction = Reaction.objects.filter(content_type=contenttype, object_id=obj_pk)

        def get_value():
            if contenttype.name == "page":
                return len(Page.objects.filter(pk=obj_pk)) != len(reaction.filter(author=request.user))
            return len(Comment.objects.filter(pk=obj_pk)) != len(reaction.filter(author=request.user))

        if serializer.is_valid() and get_value():
            self.perform_create(serializer=serializer, content_type=contenttype, obj_pk=obj_pk)
            return Response({"status":"Bày tỏ cảm xúc thành công"},status=status.HTTP_200_OK)

        return Response({"status":"Bày tỏ cảm xúc không thành công"},status=status.HTTP_400_BAD_REQUEST)
    
