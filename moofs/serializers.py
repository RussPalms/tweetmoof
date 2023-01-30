from django.conf import settings
from rest_framework import serializers
from profiles.serializers import PublicProfileSerializer
from .models import Moof

MAX_MOOF_LENGTH = settings.MAX_MOOF_LENGTH
MOOF_ACTION_OPTIONS = settings.MOOF_ACTION_OPTIONS

class MoofActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in MOOF_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for moofs.")
        return value

class MoofCreateSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True) # serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Moof
        fields = ['user', 'id', 'content', 'likes', 'timestamp']

    def get_likes(self,obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_MOOF_LENGTH:
            raise serializers.ValidationError("This moof is too long")
        return value
        
    #def get_user(self, obj):
    #    return obj.user.id


class MoofSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    parent = MoofCreateSerializer(read_only=True)

    class Meta:
        model = Moof
        fields = [
            'user', 
            'id',
            'content', 
            'likes', 
            'is_remoof', 
            'parent',
            'timestamp'
        ]

    def get_likes(self,obj):
        return obj.likes.count()

