from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, Notification
from djoser.serializers import UserSerializer 
from djoser.conf import settings

class CustomUserSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
        )
        read_only_fields = (settings.LOGIN_FIELD,)
        kwargs = {
            "write_only": {"password":True}
        }
        
    

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    object_id = serializers.ReadOnlyField()
    From = serializers.ReadOnlyField(source='From.model')
    sender = serializers.ReadOnlyField(source="sender.username")

    class Meta:
        model = Notification
        fields = "__all__"