from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, TeamInvitation

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TeamSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'leader', 'members']

class TeamInvitationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    recipient_email = serializers.EmailField(write_only=True)

    class Meta:
        model = TeamInvitation
        fields = ['id', 'sender', 'recipient', 'team', 'recipient_email', 'created_at']
        read_only_fields = ['sender', 'recipient', 'team', 'created_at']

    def create(self, validated_data):
        # This will be implemented in the view
        pass
