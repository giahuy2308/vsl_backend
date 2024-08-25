from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import Http404

from rest_framework.views import Response, status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from vsl.permissions import IsAuthorOrReadOnly
from accounts.models import Notification
from .serializers import *
from .models import *

# Create your views here.


class CommunityView(viewsets.ModelViewSet):
    # #permission_classes = [IsAuthorOrReadOnly]
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Community.objects.filter(
                (
                    Q(name__icontains=query)
                    | Q(administrator__username__icontains=query)
                ),
                is_hidden=False,
            )
        return super().get_queryset()

    def perform_create(self, serializer):
        # serializer.save(owner=self.request.user)
        community = serializer.save(owner=self.request.user)
        Participant.objects.create(
            role="admin",
            user=self.request.user,
            community=community,
        )

    @action(detail=True, methods=["post", "get"])
    def member(self, request, pk):
        if request.method == "GET":
            community = self.get_object()
            serializer = ParticipantSerializer(community.participants.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "POST":
            community = self.get_object()
            try:
                user = get_user_model().objects.get(pk=request.data["user"])
                try:
                    role = request.data["role"]
                except:
                    role = "member"
                member = Participant.objects.create(
                    user=user, role=role, community=community
                )
            except:
                return Response(
                    {"status": "Người dùng này không tồn tại"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                ParticipantSerializer(member).data, status=status.HTTP_201_CREATED
            )


class CommunityRuleView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthorOrReadOnly]
    queryset = CommunityRule.objects.all()
    serializer_class = CommunityRuleSerializer


class JoinInRequestView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthorOrReadOnly]
    queryset = JoinInRequest.objects.all()
    serializer_class = JoinInRequestSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


class ParticipantView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthorOrReadOnly]
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class PostView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query is not None:
            self.queryset = Community.objects.filter(
                Q(content__icontains=query)
                | Q(author__username__icontains=query)
                | Q(community__name__icontains=query)
            )
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReactionView(viewsets.ModelViewSet):
    # permission_classes = [IsAuthorOrReadOnly]
    queryset = Reaction.objects.all()
    serializer_class = ReactionSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
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
        serializer.save(
            content_type=content_type, object_id=obj_pk, author=self.request.user
        )

    def get_queryset(self):
        contenttype = self.request.GET.get("contenttype")
        object_id = self.request.GET.get("obj_pk")

        if contenttype is not None:
            contenttype = self.get_content_type(contenttype)
            if object_id is not None:
                self.queryset = Reaction.objects.filter(
                    content_type=contenttype, object_id=object_id
                )
            else:
                self.queryset = Reaction.objects.filter(content_type=contenttype)

        return super().get_queryset()

    def create(self, request):
        contenttype = self.get_content_type(self.request.GET.get("contenttype"))
        obj_pk = self.request.GET.get("obj_pk")
        serializer = ReactionSerializer(data=request.data)
        reaction = Reaction.objects.filter(content_type=contenttype, object_id=obj_pk)

        def get_value():
            if contenttype.name == "post":
                return len(Post.objects.filter(pk=obj_pk)) != len(
                    reaction.filter(author=request.user)
                )
            return len(Comment.objects.filter(pk=obj_pk)) != len(
                reaction.filter(author=request.user)
            )

        if serializer.is_valid() and get_value():
            self.perform_create(
                serializer=serializer, content_type=contenttype, obj_pk=obj_pk
            )
            return Response(
                {"status": "Bày tỏ cảm xúc thành công"}, status=status.HTTP_200_OK
            )

        return Response(
            {"status": "Bày tỏ cảm xúc không thành công"},
            status=status.HTTP_400_BAD_REQUEST,
        )
