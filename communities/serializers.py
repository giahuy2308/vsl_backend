from rest_framework import serializers
from .models import *


class CommunitySerializer(serializers.ModelSerializer):
    rules = serializers.SlugRelatedField(many=True, read_only=True, slug_field="title")
    owner = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = Community
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.is_show_message:
            representation["message"] = ""
        if not (instance.is_show_rule and instance.rules.all().exists()):
            representation["rules"] = []

        return representation


class CommunityRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommunityRule
        fields = "__all__"


class JoinInRequestSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        model = JoinInRequest
        fields = "__all__"


class ParticipantSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field="username")
    # community = serializers.SlugRelatedField(read_only=True, slug_field="usernam")

    class Meta:
        model = Participant
        fields = "__all__"


class ReactionSerializer(serializers.ModelSerializer):
    content_type = serializers.ReadOnlyField(source="content_type.name")
    object_id = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Reaction
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = "__all__"
