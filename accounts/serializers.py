from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user    
    

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Notification
        fields = (
            'title',
            'description',
            'user',
            'status',
            'type',
            'From',
            'created_at',
        )